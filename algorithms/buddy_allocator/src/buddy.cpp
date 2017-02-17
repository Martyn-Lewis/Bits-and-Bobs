#include <buddy.h>

#include <cmath> // pow

// Concentrating on problem solving makes for terribly barren comments.

namespace misc { namespace allocate { namespace buddy {

int pow_ceiling(int size)
{
    // Find the power of two that is at least size.
    int power = 0;
    for(int total = 1; total < size; total *= 2)
        ++power;
    return power;
}

BuddyAllocator::BuddyAllocator(size_t sz)
{
    raw_allocation = NULL;
    
    allocate(sz);
}

BuddyAllocator::~BuddyAllocator()
{
    cleanup_allocation();
}

void BuddyAllocator::cleanup_allocation()
{
    if(raw_allocation != NULL)
        ::operator delete(raw_allocation);
    allocation_tree.clear();
    raw_allocation = NULL;
}

void BuddyAllocator::allocate(size_t sz)
{
    cleanup_allocation();
    
    int power = pow_ceiling(sz);
    int true_sz = std::pow(2, power);
    
    raw_allocation = ::operator new(true_sz);
    
    allocation_tree.set_depth(power);
    allocation_tree.head.pointer = raw_allocation;
}

bool recursive_truly_free(BuddyNode* with)
{
    if(with->has_left())
    {
        BuddyNode* left = with->left();
        if(left->allocated)
            return false;
        if(!recursive_truly_free(left))
            return false;
    }
    
    if(with->has_right())
    {
        BuddyNode* right = with->right();
        if(right->allocated)
            return false;
        if(!recursive_truly_free(right))
            return false;
    }
    
    return true;
}

BuddyNode* recursive_find_free_node(BuddyNode* with, int depth_for)
{
    if(with->depth == depth_for && !with->allocated)
    {
        if(with->depth == 0)
            return with;
        
        if(!recursive_truly_free(with))
            return NULL;
            
        return with;
    }
    
    if(with->allocated)
        return NULL;
    
    if(with->depth - 1 < depth_for)
        return NULL;
    
    BuddyNode* left = recursive_find_free_node(with->left(), depth_for);
    if(left != NULL)
        return left;
    else
        return recursive_find_free_node(with->right(), depth_for);
}

BuddyNode* BuddyAllocator::find_minimum_node(size_t sz)
{
    int target_power = pow_ceiling(sz);
    return recursive_find_free_node(&allocation_tree.head, target_power);
}

BuddyNode* recursive_find_node_from_ptr(BuddyNode* with, void* ptr_for)
{
    if(ptr_for >= with->pointer && ptr_for < with->pointer + (size_t)std::pow(2, with->depth))
    {
        if(with->allocated)
            return with;
        // Otherwise it's the left or right, so continue as usual.
    }
    
    if(with->has_left()) {
        BuddyNode* left = recursive_find_node_from_ptr(with->left(), ptr_for);
        if(left != NULL)
            return left;
    }
    
    if(with->has_right())
    {
        return recursive_find_node_from_ptr(with->right(), ptr_for);
    }
    
    return NULL;
}

BuddyNode* BuddyAllocator::find_node_from_ptr(void* ptr)
{
    return recursive_find_node_from_ptr(&allocation_tree.head, ptr);
}

void* BuddyAllocator::alloc(size_t sz)
{
    BuddyNode* free_node = find_minimum_node(sz);
    
    if(free_node == NULL)
        throw "Buddy Allocator does not have enough free memory to satisfy allocation.";
    
    free_node->allocated = true;
    return free_node->pointer;
}

void BuddyAllocator::free(void* ptr)
{
    void* base = allocation_tree.head.pointer;
    size_t difference = (size_t) ((char*)ptr - (char*)base);
    if(difference < 0 || difference > pow(2, allocation_tree.head.depth))
        throw "Attempted to free invalid pointer!";
    
    BuddyNode* node = find_node_from_ptr(ptr);
    if(node == NULL)
        throw "Unable to find given allocation to free it up.";
        
    if(!node->allocated) // This should technically never happen.
        throw "Potential double free on the same allocation.";
    
    node->allocated = false;
}

}}}
