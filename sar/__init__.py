#!/usr/bin/env python


"""Indicates CPU part of SAR file"""
PART_CPU = 0

"""Indicates RAM memory usage part of SAR file"""
PART_MEM = 1

"""Indicates swap memory usage part of SAR file"""
PART_SWP = 2

"""I/O usage part of SAR file"""
PART_IO = 3

"""Paging stats of SAR file"""
PART_PAGING = 4

"""Network usage part of SAR file"""
PART_NET = 5

"""CPU regexp pattern for detecting SAR section header"""
PATTERN_CPU = ".*CPU.*(usr|user).*nice.*sys.*"

"""Regexp terms for finding fields in SAR parts for CPU"""
FIELDS_CPU = [
    '\%(usr|user)', '\%nice', '\%sys', '\%iowait', '\%idle'
]

"""Pair regexp terms with field names in CPU output dictionary"""
FIELD_PAIRS_CPU = {
    'usr': FIELDS_CPU[0], 'nice': FIELDS_CPU[1], 'sys': FIELDS_CPU[2],
    'iowait': FIELDS_CPU[3], 'idle': FIELDS_CPU[4]
}

"""Mem usage regexp pattern for detecting SAR section header"""
PATTERN_MEM = ".*kbmemfree.*kbmemused.*memused.*kbbuffers.*kbcached.*"

"""Regexp terms for finding fields in SAR parts for memory usage"""
FIELDS_MEM = [
    'kbmemfree', 'kbmemused', '\%memused', 'kbbuffers', 'kbcached'
]

"""Pair regexp terms with field names in memory usage output dictionary"""
FIELD_PAIRS_MEM = {
    'memfree': FIELDS_MEM[0], 'memused': FIELDS_MEM[1],
    'memusedpercent': FIELDS_MEM[2], 'membuffer': FIELDS_MEM[3],
    'memcache': FIELDS_MEM[4]
}

"""Swap usage regexp pattern for detecting SAR section header"""
PATTERN_SWP = ".*kbswpfree.*kbswpused.*swpused.*"

"""Regexp terms for finding fields in SAR parts for swap usage"""
FIELDS_SWP = [
    'kbswpfree', 'kbswpused', '\%swpused'
]

"""Pair regexp terms with field names in swap usage output dictionary"""
FIELD_PAIRS_SWP = {
    'swapfree': FIELDS_SWP[0], 'swapused': FIELDS_SWP[1],
    'swapusedpercent': FIELDS_SWP[2]
}

"""I/O usage regexp pattern for detecting SAR section header"""
PATTERN_IO = ".*tps.*rtps.*wtps.*bread\/s.*bwrtn\/s.*"

"""Regexp terms for finding fields in SAR parts for swap usage"""
FIELDS_IO = [
    '^tps', '^rtps', '^wtps', 'bread\/s', 'bwrtn\/s'
]

"""Pair regexp terms with field names in swap usage output dictionary"""
FIELD_PAIRS_IO = {
    'tps': FIELDS_IO[0], 'rtps': FIELDS_IO[1], 'wtps': FIELDS_IO[2],
    'bread': FIELDS_IO[3], 'bwrite': FIELDS_IO[4],

}

"""Paging stats regexp pattern for detecting SAR section header"""
PATTERN_PAGING = ".*pgpgin\/s.*pgpgout\/s.*fault\/s.*majflt\/s.*pgfree\/s.*pgscank\/s.*pgscand\/s.*pgsteal\/s.*\%vmeff.*"

"""Regexp terms for finding fields in SAR parts for paging statistics"""
FIELDS_PAGING = [
    '^pgpgin\/s', '^pgpgout\/s', '^fault\/s', '^majflt\/s', '^pgfree\/s', 'pgscank\/s', 'pgscand\/s', 'pgsteal\/s', '\%vmeff'
]

"""Pair regexp terms with field names in paging status output dictionary"""
FIELD_PAIRS_PAGING = {
    'pgpgin': FIELDS_PAGING[0], 'pgpgout': FIELDS_PAGING[1], 'fault': FIELDS_PAGING[2],
    'majflt': FIELDS_PAGING[3], 'pgfree': FIELDS_PAGING[4], 'pgscank': FIELDS_PAGING[5],
    'pgscand': FIELDS_PAGING[6], 'pgsteal': FIELDS_PAGING[7], 'vmeff': FIELDS_PAGING[8]
}

"""Network usage regexp pattern for detecting SAR section header"""
PATTERN_NET = ".*IFACE.*rxpck\/s.*txpck\/s.*rxkB\/s.*txkB\/s.*rxcmp\/s.*txcmp\/s.*rxmcst\/s.*"

"""Regexp terms for finding fields in SAR parts for paging statistics"""
FIELDS_NET = [
    '^IFACE', '^rxpck\/s', '^txpck\/s', '^rxkB\/s', '^txkB\/s', '^rxcmp\/s', 'txcmp\/s', 'rxmcst\/s'
]

"""Pair regexp terms with field names in paging status output dictionary"""
FIELD_PAIRS_NET = {
    'iface': FIELDS_NET[0], 'rxpck': FIELDS_NET[1], 'txpck': FIELDS_NET[2], 
    'rxkB': FIELDS_NET[3], 'txkB': FIELDS_NET[4], 'rxcmp': FIELDS_NET[5], 
    'txcmp': FIELDS_NET[6], 'rxmcst': FIELDS_NET[7]
}

"""Restart time regexp pattern for detecting SAR restart notices"""
PATTERN_RESTART = ".*LINUX\ RESTART.*"

"""Pattern for splitting multiple combined SAR file"""
PATTERN_MULTISPLIT = "Linux"

"""Split by date in multiday SAR file"""
PATTERN_DATE = "[0-9][0-9][0-9][0-9]\-[0-9][0-9]\-[0-9][0-9]"

__all__ = [
    "PART_CPU", "PART_MEM", "PART_SWP", "PART_IO",
    "PATTERN_CPU", "PATTERN_MEM", "PATTERN_SWP", "PATTERN_IO",
    "PATTERN_RESTART", "PATTERN_MULTISPLIT", "PATTERN_DATE"
]
