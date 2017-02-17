#ifndef __MISC_SORT_SORTED__H
    #define __MISC_SORT_SORTED__H

    #include <vector>
    
    namespace misc {
        namespace sort {
            template<typename T, typename A> bool sorted(std::vector<T, A>& items)
            {
                // Determines if the given vector is sorted.
                // O(n) on a sorted vector.
                int length = items.size();
                
                if(length <= 1)
                    return true;
                    
                for(typename std::vector<T, A>::iterator it = items.begin() + 1; it < items.end(); ++it)
                    if(*it < *(it - 1))
                        return false;
                        
                return true;
            }
        }
    }
#endif // __MISC_SORT_SORTED__H
