#ifndef __MISC__ALLOCATE_BUDDY_NODE__H
    #define __MISC__ALLOCATE_BUDDY_NODE__H
    
    #include <cstdlib>
    
    namespace misc { namespace allocate { namespace buddy {
        class BuddyNode {
            BuddyNode* raw_left;
            BuddyNode* raw_right;
            
        public:
            int depth;
            bool allocated;
            void* pointer;
        
            BuddyNode();
            ~BuddyNode();
            
            BuddyNode* left();
            BuddyNode* right();
            
            void clear_left();
            void clear_right();
            
            bool has_left();
            bool has_right();
            
            size_t size();
        };
    }}}
#endif // __MISC__ALLOCATE_BUDDY_NODE__H
