#include <buddy_tree.h>

namespace misc { namespace allocate { namespace buddy {

BuddyTree::BuddyTree()
{
}

BuddyTree::~BuddyTree()
{
}

void BuddyTree::clear()
{
    head.clear_left();
    head.clear_right();
}

void BuddyTree::set_depth(int depth)
{
    head.depth = depth;
}

}}}
