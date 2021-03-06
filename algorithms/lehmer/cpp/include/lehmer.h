#ifndef __MISC_RANDOM_LEHMER__H
    #define __MISC_RANDOM_LEHMER__H
    
    #if __cplusplus > 199711L
        #include <cstdint>
    #else
        #include <stdint.h>
    #endif
    
    namespace misc {
        namespace random {
            uint32_t lehmer_random(uint32_t seed);
            uint32_t lehmer_random(uint32_t seed, uint64_t g, uint64_t modulo);
        }
    }
    
#endif // __MISC_RANDOM_LEHMER__H
