#include <naive_search.h>


namespace misc { namespace string {
    int naive_search_first(std::string haystack, std::string needle)
    {
        // Find the first instance of needle within haystack.
        if(haystack.length() < needle.length())
            return -1;
        
        for(int offset = 0; offset <= haystack.length() - needle.length(); ++offset)
        {
            if(haystack.compare(offset, needle.length(), needle) == 0)
                return offset;
        }
        
        return -1;
    }
    
    int naive_search_last(std::string haystack, std::string needle)
    {
        // Find the last instance of needle within haystack.
        if(haystack.length() < needle.length())
            return -1;
        
        for(int offset = haystack.length() - needle.length(); offset >= 0; --offset)
        {
            if(haystack.compare(offset, needle.length(), needle) == 0)
                return offset;
        }
        
        return -1;
    }
    
    std::vector<int> naive_search_all(std::string haystack, std::string needle)
    {
        // Find all instances of needle within haystack.
        std::vector<int> result;
        
        if(haystack.length() < needle.length())
            return result;
        
        for(int offset = 0; offset <= haystack.length() - needle.length(); ++offset)
        {
            if(haystack.compare(offset, needle.length(), needle) == 0)
                result.push_back(offset);
        }
        
        return result;
    }
}}
