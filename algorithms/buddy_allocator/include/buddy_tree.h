#ifndef __MISC__ALLOCATE_BUDDY_TREE__H
    #define __MISC__ALLOCATE_BUDDY_TREE__H
    
    #include <buddy_node.h>
    
    namespace misc { namespace allocate { namespace buddy {
        class BuddyTree {
            int depth;
        public:
            BuddyNode head;
        
            void clear();
            void set_depth(int depth);
            
            BuddyTree();
            ~BuddyTree();
        };
    }}}
    
#endif // __MISC__ALLOCATE_BUDDY_TREE__H
