#include <buddy_node.h>

#include <cmath> // pow.

namespace misc { namespace allocate { namespace buddy {

BuddyNode::BuddyNode()
{
    raw_left = NULL;
    raw_right = NULL;
    
    allocated = false;
    pointer = NULL;
    depth = 0;
}

BuddyNode::~BuddyNode()
{
    clear_left();
    clear_right();
}

BuddyNode* BuddyNode::left()
{
    if(raw_left == NULL) {
        raw_left = new BuddyNode();
        raw_left->pointer = pointer;
        raw_left->depth = depth - 1;
    }
    return raw_left;
}

BuddyNode* BuddyNode::right()
{
    if(raw_right == NULL) {
        raw_right = new BuddyNode();
        raw_right->pointer = this->pointer + (size_t)std::pow(2, depth - 1);
        raw_right->depth = depth - 1;
    }
    return raw_right;
}

void BuddyNode::clear_left()
{
    if(raw_left != NULL)
        delete raw_left;
    raw_left = NULL;
}

void BuddyNode::clear_right()
{
    if(raw_right != NULL)
        delete raw_right;
    raw_right = NULL;
}

bool BuddyNode::has_left()
{
    return raw_left != NULL;
}

bool BuddyNode::has_right()
{
    return raw_right != NULL;
}

size_t BuddyNode::size()
{
    return std::pow(2, depth);
}

}}}
