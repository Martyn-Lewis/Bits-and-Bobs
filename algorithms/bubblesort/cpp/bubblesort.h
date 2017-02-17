#ifndef __MISC_SORT_BUBBLESORT__H
    #define __MISC_SORT_BUBBLESORT__H

    #if __cplusplus > 199711L
        #include <utility>
    #else
        #include <algorithm>
    #endif
    
    #include <vector>
    
    namespace misc {
        namespace sort {
            template<class T> void bubblesort(std::vector<T>& items)
            {
                // Currently has two optimisations:
                // ---
                //    The last swap of the last run is equivelant to the last item in need of a sort.
                //    So the next run will only need to both up until that last swap's index.
                // ---
                //    Cocktail shaking is implemented in an attempt to turn turtles into hares on alternate cycles.
                if(items.size() <= 1)
                    return;
                
                int start = 1;
                int end = items.size();
                
                bool has_sorted;
                do {
                    has_sorted = false;
                    int new_start = end;
                    int new_end = start;
                    if(start < end) {
                        for(int n = start; n < end; ++n) {
                            if(items[n-1] > items[n]) {
                                std::swap(items[n-1], items[n]);
                                has_sorted = true;
                                new_start = n;
                            }
                        }
                    } else {
                        for(int n = start; n > end; --n) {
                            if(items[n-1] > items[n]) {
                                std::swap(items[n-1], items[n]);
                                has_sorted = true;
                                new_end = n;
                            }
                        }
                    }
                    start = new_start;
                    end = new_end;
                    std::swap(start, end);
                } while(has_sorted);
            }
        }
    }
#endif // __MISC_SORT_BUBBLESORT__H
