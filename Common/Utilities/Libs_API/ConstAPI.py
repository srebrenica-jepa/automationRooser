# - Smart Rules
URL_SR_PREFIX = 'latest/policy/protection-profile/{0}/smart-rule/'
URL_SR_SERVICE_UDP_BIT = URL_SR_PREFIX + 'service/udp/bit-rate'
URL_SR_SERVICE_UDP_PACKET = URL_SR_PREFIX + 'service/udp/packet-rate'
URL_SR_SERVICE_TCP_SYN_BIT = URL_SR_PREFIX + 'service/tcp-syn/bit-rate'
URL_SR_SERVICE_TCP_SYN_PACKET = URL_SR_PREFIX + 'service/tcp-syn/packet-rate'
URL_SR_SERVICE_TCP_RST_BIT = URL_SR_PREFIX + 'service/tcp-rst/bit-rate'
URL_SR_SERVICE_TCP_RST_PACKET = URL_SR_PREFIX + 'service/tcp-rst/packet-rate'
URL_SR_SERVICE_TCP_DATA_BIT = URL_SR_PREFIX + 'service/tcp-data/bit-rate'
URL_SR_SERVICE_TCP_DATA_PACKET = URL_SR_PREFIX + 'service/tcp-data/packet-rate'
URL_SR_SERVICE_ICMP_BIT = URL_SR_PREFIX + 'service/icmp/bit-rate'
URL_SR_SERVICE_ICMP_DATA_PACKET = URL_SR_PREFIX + 'service/icmp/packet-rate'
URL_SR_REFLECTION_UDP_BIT = URL_SR_PREFIX + 'reflection/udp-or-icmp/bit-rate'
URL_SR_REFLECTION_UDP_PACKET = URL_SR_PREFIX + 'reflection/udp-or-icmp/packet-rate'
URL_SR_REFLECTION_UDP_53_BIT = URL_SR_PREFIX + 'reflection/udp-source-port-53/bit-rate'
URL_SR_REFLECTION_UDP_53_PACKET = URL_SR_PREFIX + 'reflection/udp-source-port-53/packet-rate'
URL_SR_REFLECTION_UDP_4500_BIT = URL_SR_PREFIX + 'reflection/udp-source-port-4500/bit-rate'
URL_SR_REFLECTION_UDP_4500_PACKET = URL_SR_PREFIX + 'reflection/udp-source-port-4500/packet-rate'
URL_SR_REFLECTION_DNS =  URL_SR_PREFIX + 'reflection/dns-query-response'
URL_SR_REFLECTION_DNS_BIT = URL_SR_PREFIX + 'reflection/dns-query-response/bit-rate'
URL_SR_REFLECTION_DNS_PACKET = URL_SR_PREFIX + 'reflection/dns-query-response/packet-rate'
URL_SR_REFLECTION_TCP_SYN_ACK_BIT = URL_SR_PREFIX + 'reflection/tcp-syn-ack/bit-rate'
URL_SR_REFLECTION_TCP_SYN_ACK_PACKET = URL_SR_PREFIX + 'reflection/tcp-syn-ack/packet-rate'
URL_SR_REFLECTION_TCP_RST_BIT = URL_SR_PREFIX + 'reflection/tcp-rst/bit-rate'
URL_SR_REFLECTION_TCP_RST_PACKET = URL_SR_PREFIX + 'reflection/tcp-rst/packet-rate'
URL_SR_REFLECTION_TCP_ACK_PSH_BIT = URL_SR_PREFIX + 'reflection/tcp-ack-psh/bit-rate'
URL_SR_REFLECTION_TCP_ACK_PSH_PACKET = URL_SR_PREFIX + 'reflection/tcp-ack-psh/packet-rate'
URL_SR_SERVER_ANY_BIT = URL_SR_PREFIX + 'server/non-tcp/bit-rate'
URL_SR_SERVER_ANY_PACKET = URL_SR_PREFIX + 'server/non-tcp/packet-rate'
URL_SR_SERVER_ANY_FRAGMENT_BIT = URL_SR_PREFIX + 'server/udp-fragment-under-attack/bit-rate'
URL_SR_SERVER_ANY_FRAGMENT_PACKET = URL_SR_PREFIX + 'server/udp-fragment-under-attack/packet-rate'
URL_SR_SOURCE_IP_ADDRESS_BIT = URL_SR_PREFIX + 'source/ip-address/bit-rate'
URL_SR_SOURCE_IP_ADDRESS_PACKET = URL_SR_PREFIX + 'source/ip-address/packet-rate'
URL_SR_ICMP_FAILED_REFLECTORS_BIT = URL_SR_PREFIX + 'icmp/icmp-from-failed-reflectors/bit-rate'
URL_SR_ICMP_FAILED_REFLECTORS_PACKET = URL_SR_PREFIX + 'icmp/icmp-from-failed-reflectors/packet-rate'
URL_SR_ICMP_UDP_DEST_PORT = URL_SR_PREFIX + 'icmp/dest-port'
URL_SR_ICMP_UDP_DEST_PORT_SINGLE = URL_SR_ICMP_UDP_DEST_PORT + '/{1}'
URL_SR_ICMP_V4_TYPE = URL_SR_PREFIX + 'icmp/v4-type'
URL_SR_ICMP_V4_TYPE_SINGLE = URL_SR_ICMP_V4_TYPE + '/{1}'
URL_SR_ICMP_V6_TYPE = URL_SR_PREFIX + 'icmp/v6-type'
URL_SR_ICMP_V6_TYPE_SINGLE = URL_SR_ICMP_V6_TYPE + '/{1}'
URL_PP = 'latest/policy/protection-profile'
URL_PP_SINGLE = URL_PP + '/{0}'

URL_FR_DETECT = 'latest/policy/protection-profile/{0}/flex-rule-blocking/detect-only'
URL_FR_DETECT_FILTERS = 'latest/policy/protection-profile/{0}/flex-rule-blocking/detect-only/filter'
URL_FR_DETECT_FILTER = URL_FR_DETECT_FILTERS + '/{1}'

URL_FR_BLOCK = 'latest/policy/protection-profile/{0}/flex-rule-blocking/block-only'
URL_FR_BLOCK_FILTER = 'latest/policy/protection-profile/{0}/flex-rule-blocking/block-only/filter'
URL_FR_BLOCK_FILTER_SINGLE = URL_FR_BLOCK_FILTER + '/{1}'

URL_FR_PROG_RULES = 'latest/policy/protection-profile/{0}/flex-rule-blocking/programmable/'
URL_FR_PROG_RULE = 'latest/policy/protection-profile/{0}/flex-rule-blocking/programmable/{1}/'
URL_FR_PROG_FILTERS = 'latest/policy/protection-profile/{0}/flex-rule-blocking/programmable/filter'
URL_FR_PROG_FILTER = URL_FR_PROG_FILTERS + '/{1}'
URL_FR_PROG_FILTERS_V2 = 'latest/policy/protection-profile/{0}/flex-rule-blocking/programmable/{1}/filter/'
URL_FR_PROG_FILTER_V2 = URL_FR_PROG_FILTERS_V2 + '{2}'

URL_FR_GENERAL_V2 = 'latest/policy/protection-profile/{0}/flex-rule-blocking/general/'
URL_FR_GENERAL_FILTER_V2 = URL_FR_GENERAL_V2 + '{1}/filter/'
URL_FR_GENERAL_FILTER_SINGLE_V2 = URL_FR_GENERAL_FILTER_V2 + '{2}'

URL_FR_IP_TABLE = URL_PP + '/{0}/flex-rule-blocking/ip-table'
URL_FR_IP_TABLE_ADDRESS_GROUP = URL_FR_IP_TABLE + '/{1}/address-group'

URL_IC_ENTRIES = 'latest/policy/protection-profile/{0}/inspection-control/override-entry'
URL_IC_ENTRY = URL_IC_ENTRIES + '/{1}'
URL_IC_DESTINATION_IPS = URL_PP + '/{0}/inspection-control/override-entry/{1}/destination-ip'
URL_IC_DESTINATION_IP = URL_IC_DESTINATION_IPS + '/{2}'
URL_IC_DESTINATION_GROUPS = URL_PP + '/{0}/inspection-control/override-entry/{1}/destination-group'
URL_IC_DESTINATION_GROUP = URL_IC_DESTINATION_GROUPS + '/{2}'
URL_ISC_ENTRIES = 'latest/policy/protection-profile/{0}/source-control/entry'
URL_ISC_ENTRY = URL_ISC_ENTRIES + '/{1}'
URL_ISC_SOURCE_IP = URL_ISC_ENTRIES + '/{1}/source-ip'
URL_ISC_SOURCE_IP_SINGLE = URL_ISC_SOURCE_IP + '/{2}'
URL_ISC_SOURCE_IP_GROUP = URL_ISC_ENTRIES + '/{1}/source-group'
URL_ISC_SOURCE_IP_GROUP_SINGLE = URL_ISC_SOURCE_IP_GROUP + '/{2}'
URL_ADDRESS_GROUP = 'latest/policy/address-group'
URL_ADDRESS_GROUP_SINGLE = URL_ADDRESS_GROUP + '/{0}'
URL_AG_IP = 'latest/policy/address-group/{0}/ip'
URL_AG_IP_SINGLE = URL_AG_IP + '/{1}'
URL_TA_GLOBAL = 'latest/policy/protection-profile/{0}/threat-awareness/global'
URL_TA_GLOBAL_ACT_THRESHOLDS = URL_TA_GLOBAL + '/activation-thresholds'
URL_TA_GLOBAL_EXIT_THRESHOLDS = URL_TA_GLOBAL + '/exit-thresholds'
URL_TA = 'latest/policy/protection-profile/{0}/threat-awareness'
URL_TA_TCP_DESTINATION = URL_TA + '/destination-tcp'
URL_TA_TCP_SYN_BIT_RATE = URL_TA_TCP_DESTINATION + '/tcp-syn/bit-rate'
URL_TA_TCP_SYN_PACKET_RATE = URL_TA_TCP_DESTINATION + '/tcp-syn/packet-rate'
URL_TA_TCP_RST_BIT_RATE = URL_TA_TCP_DESTINATION + '/tcp-rst/bit-rate'
URL_TA_TCP_RST_PACKET_RATE = URL_TA_TCP_DESTINATION + '/tcp-rst/packet-rate'
URL_TA_TCP_ACK_BIT_RATE = URL_TA_TCP_DESTINATION + '/tcp/bit-rate'
URL_TA_TCP_ACK_PACKET_RATE = URL_TA_TCP_DESTINATION + '/tcp/packet-rate'
URL_TA_NON_TCP_DESTINATION = URL_TA + '/destination-non-tcp'
URL_TA_NON_TCP_BIT_RATE = URL_TA_NON_TCP_DESTINATION + '/non-tcp/bit-rate'
URL_TA_NON_TCP_PACKET_RATE = URL_TA_NON_TCP_DESTINATION + '/non-tcp/packet-rate'
URL_PSM_SOURCE_RULES = URL_SR_PREFIX + 'source/programmable'
URL_PSM_SOURCE_RULES_SINGLE = URL_PSM_SOURCE_RULES + '/{1}'
URL_PSM_SOURCE_BIT_RATE = URL_PSM_SOURCE_RULES_SINGLE + '/bit-rate'
URL_PSM_SOURCE_PACKET_RATE = URL_PSM_SOURCE_RULES_SINGLE + '/packet-rate'
URL_PSM_SOURCE_CUSTOM_MATCH = URL_PSM_SOURCE_RULES_SINGLE + '/custom-match'
URL_PSM_SOURCE_CUSTOM_MATCH_SINGLE = URL_PSM_SOURCE_CUSTOM_MATCH + '/{2}'
URL_PSM_REFLECTION_RULES = URL_SR_PREFIX + 'reflection/programmable'
URL_PSM_REFLECTION_RULES_SINGLE = URL_PSM_REFLECTION_RULES + '/{1}'
URL_PSM_REFLECTION_BIT_RATE = URL_PSM_REFLECTION_RULES_SINGLE + '/bit-rate'
URL_PSM_REFLECTION_PACKET_RATE = URL_PSM_REFLECTION_RULES_SINGLE + '/packet-rate'
URL_PSM_REFLECTION_CUSTOM_MATCH = URL_PSM_REFLECTION_RULES_SINGLE + '/custom-match'
URL_PSM_REFLECTION_CUSTOM_MATCH_SINGLE = URL_PSM_REFLECTION_CUSTOM_MATCH + '/{2}'
URL_PSM_SERVICE_RULES = URL_SR_PREFIX + 'service/programmable'
URL_PSM_SERVICE_RULES_SINGLE = URL_PSM_SERVICE_RULES + '/{1}'
URL_PSM_SERVICE_BIT_RATE = URL_PSM_SERVICE_RULES_SINGLE + '/bit-rate'
URL_PSM_SERVICE_PACKET_RATE = URL_PSM_SERVICE_RULES_SINGLE + '/packet-rate'
URL_PSM_SERVICE_CUSTOM_MATCH = URL_PSM_SERVICE_RULES_SINGLE + '/custom-match'
URL_PSM_SERVICE_CUSTOM_MATCH_SINGLE = URL_PSM_SERVICE_CUSTOM_MATCH + '/{2}'
URL_PSM_SERVER_RULES = URL_SR_PREFIX + 'server/programmable'
URL_PSM_SERVER_RULES_SINGLE = URL_PSM_SERVER_RULES + '/{1}'
URL_PSM_SERVER_BIT_RATE = URL_PSM_SERVER_RULES_SINGLE + '/bit-rate'
URL_PSM_SERVER_PACKET_RATE = URL_PSM_SERVER_RULES_SINGLE + '/packet-rate'
URL_PSM_SERVER_CUSTOM_MATCH = URL_PSM_SERVER_RULES_SINGLE + '/custom-match'
URL_PSM_SERVER_CUSTOM_MATCH_SINGLE = URL_PSM_SERVER_CUSTOM_MATCH + '/{2}'
URL_PSM_ICMP_RULES = URL_SR_PREFIX + 'icmp/programmable'
URL_PSM_ICMP_RULES_SINGLE = URL_PSM_ICMP_RULES + '/{1}'
URL_PSM_ICMP_BIT_RATE = URL_PSM_ICMP_RULES_SINGLE + '/bit-rate'
URL_PSM_ICMP_PACKET_RATE = URL_PSM_ICMP_RULES_SINGLE + '/packet-rate'
URL_PSM_ICMP_CUSTOM_MATCH = URL_PSM_ICMP_RULES_SINGLE + '/custom-match'
URL_PSM_ICMP_CUSTOM_MATCH_SINGLE = URL_PSM_ICMP_CUSTOM_MATCH + '/{2}'
URL_CSM_SERVICE = URL_SR_PREFIX + 'service/custom'
URL_CSM_SERVICE_SINGLE = URL_CSM_SERVICE + '/{1}'
URL_CSM_SERVICE_DPORTS = URL_CSM_SERVICE_SINGLE + '/destination-ports'
URL_CSM_SERVICE_DPORT = URL_CSM_SERVICE_DPORTS + '/{2}'
URL_CSM_SERVICE_PACKET = URL_CSM_SERVICE_SINGLE + '/packet-rate'
URL_CSM_SERVICE_BIT = URL_CSM_SERVICE_SINGLE + '/bit-rate'
URL_CSM_REFLECTION = URL_SR_PREFIX + 'reflection/custom'
URL_CSM_REFLECTION_SINGLE = URL_CSM_REFLECTION + '/{1}'
URL_CSM_REFLECTION_SPORTS = URL_CSM_REFLECTION_SINGLE + '/source-ports'
URL_CSM_REFLECTION_SPORT = URL_CSM_REFLECTION_SPORTS + '/{2}'
URL_CSM_REFLECTION_PACKET = URL_CSM_REFLECTION_SINGLE + '/packet-rate'
URL_CSM_REFLECTION_BIT = URL_CSM_REFLECTION_SINGLE + '/bit-rate'
URL_CSM_SERVER = URL_SR_PREFIX + 'server/custom'
URL_CSM_SERVER_SINGLE = URL_CSM_SERVER + '/{1}'
URL_CSM_SERVER_PROTOCOLS = URL_CSM_SERVER_SINGLE + '/protocols'
URL_CSM_SERVER_PROTOCOL = URL_CSM_SERVER_PROTOCOLS + '/{2}'
URL_CSM_SERVER_PACKET = URL_CSM_SERVER_SINGLE + '/packet-rate'
URL_CSM_SERVER_BIT = URL_CSM_SERVER_SINGLE + '/bit-rate'

URL_PACKET_RULES = '/latest/policy/protection-profile/{0}/packet-rules/{1}'

# Advanced Settings
URL_AS_PREFIX = '/latest/policy/protection-profile/{0}/advanced-settings'
URL_AS_FRAGMENTATION = URL_AS_PREFIX + '/fragmentation'
URL_AS_ICMP_RATE_LIMITS = URL_AS_PREFIX + '/icmp-rate-limits'
URL_AS_LOAD_BALANCE_CONTROLS = URL_AS_PREFIX + '/load-balance-controls'
URL_AS_PROBATION_CONTROL = URL_AS_PREFIX + '/probation-controls'
URL_AS_UDP_RATE_LIMITS = URL_AS_PREFIX + '/udp-rate-limits'
URL_AS_NTD120_INGRESS_LOAD_LEVEL = URL_AS_PREFIX + '/ntd120-ingress-load-level'