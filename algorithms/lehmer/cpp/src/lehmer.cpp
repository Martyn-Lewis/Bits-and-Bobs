#include <lehmer.h>

namespace misc {
    namespace random {
        uint32_t lehmer_random(uint32_t seed, uint64_t g, uint64_t modulo)
        {
            return ((uint64_t)seed * g) % modulo;
        }
    
        uint32_t lehmer_random(uint32_t seed)
        {
            return lehmer_random(seed, (uint64_t)279470273UL, (uint64_t)4294967291UL);
        }
    }
}
