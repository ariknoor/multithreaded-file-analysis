# Test Cases
## Multithreaded File Analysis and Performance Evaluation

| Test ID | Test Scenario | Input | Expected Result |
|---------|---------------|-------|-----------------|
| TC-01 | Sequential analysis | WARNING with 8 small files | 80,000 total occurrences |
| TC-02 | Multithreaded analysis | WARNING with 1 thread and 8 small files | 80,000 total occurrences |
| TC-03 | Two-thread analysis | WARNING with 2 threads and 8 small files | 80,000 total occurrences |
| TC-04 | Four-thread analysis | WARNING with 4 threads and 8 small files | 80,000 total occurrences |
| TC-05 | Eight-thread analysis | WARNING with 8 threads and 8 small files | 80,000 total occurrences |
| TC-06 | Medium dataset | WARNING with 8 medium files | 400,000 total occurrences |
| TC-07 | Large dataset | WARNING with 8 large files | 800,000 total occurrences |
| TC-08 | Race condition | Two threads increment shared counter | Actual value may differ from expected value |
| TC-09 | Mutex synchronization | Two threads increment protected counter | Expected and actual values should match |
| TC-10 | Invalid thread count | Thread count = 0 | Error message should be displayed |
| TC-11 | Missing file | Provide a nonexistent filename | File opening error should be displayed |
| TC-12 | No matching target | Search for a nonexistent target | Zero occurrences should be reported for readable files |

## Test Execution Notes

- Functional tests verify the occurrence counts.
- Performance tests use five measurements per configuration.
- Race condition and mutex programs demonstrate synchronization behavior.
- Invalid-input tests verify basic error handling.

## Final Test Execution Results

TC-10: Invalid thread count (0) - PASS
TC-11: Missing file - PASS
TC-12: No matching target word - PASS
