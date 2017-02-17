#ifndef __MISC_STRING_NAIVE_SEARCH__H
    #define __MISC_STRING_NAIVE_SEARCH__H
    
    #include <string>
    #include <vector>
    
    namespace misc {
        namespace string {
            int naive_search_first(std::string haystack, std::string needle);
            int naive_search_last(std::string haystack, std::string needle);
            std::vector<int> naive_search_all(std::string haystack, std::string needle);
        }
    }
    
#endif // __MISC_STRING_NAIVE_SEARCH__H
