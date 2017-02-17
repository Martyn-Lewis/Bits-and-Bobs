#ifndef __MISC_SORT_INSERTIONSORT__H
    #define __MISC_SORT_INSERTIONSORT__H

    #if __cplusplus > 199711L
        #include <utility>
    #else
        #include <algorithm>
    #endif
    
    #include <vector>
    
    namespace misc {
        namespace sort {
            template<class T> void insertionsort(std::vector<T>& items)
            {
                if(items.size() <= 1)
                    return;
                
                for(int i = 1; i < items.size(); ++i)
                {
                    T displacee = items[i];
                    
                    int displace_index = i - 1;
                    while(displace_index >= 0 && items[displace_index] > displacee)
                    {
                        items[displace_index + 1] = items[displace_index];
                        displace_index--;
                    }
                    
                    items[displace_index + 1] = displacee;
                }
            }
        }
    }
#endif // __MISC_SORT_INSERTIONSORT__H
