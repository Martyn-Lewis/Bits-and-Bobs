#ifndef __MISC__ALLOCATE_BUDDY__H
    #define __MISC__ALLOCATE_BUDDY__H
    
    #include <buddy_tree.h>
    
    #include <cstdlib>
    
    namespace misc { namespace allocate { namespace buddy {  
        class BuddyAllocator {
        private:
            void* raw_allocation;
            
            void allocate(size_t sz);
            void cleanup_allocation();
            
            BuddyNode* find_minimum_node(size_t sz);
            BuddyNode* find_node_from_ptr(void* ptr);
            
        public:
            BuddyTree allocation_tree;
        
            BuddyAllocator(size_t sz);
            ~BuddyAllocator();
            
            void* alloc(size_t sz);
            void free(void* ptr);
        };
    }}}
#endif // __MISC__ALLOCATE_BUDDY__H
