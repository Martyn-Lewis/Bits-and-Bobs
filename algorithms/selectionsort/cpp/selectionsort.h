#ifndef __MISC_SORT_SELECTIONSORT__H
    #define __MISC_SORT_SELECTIONSORT__H

    #if __cplusplus > 199711L
        #include <utility>
    #else
        #include <algorithm>
    #endif
    
    #include <vector>
    
    namespace misc {
        namespace sort {
            template<class T> void selectionsort(std::vector<T>& items)
            {
                if(items.size() <= 1)
                    return;
                
                for(int i = 0; i < items.size(); ++i)
                {
                    T old = items[i];
                    T minimum = old;
                    int index = i;
                    
                    for(int n = i; n < items.size(); ++n)
                    {
                        if(items[n] < minimum)
                        {
                            index = n;
                            minimum = items[n];
                        }
                    }
                    
                    if(minimum < old)
                        std::swap(items[index], items[i]);
                }
            }
        }
    }
#endif // __MISC_SORT_SELECTIONSORT__H
