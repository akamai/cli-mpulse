
# public API key for demo (may not support all report types)
KEY = PH7E4-H9YBZ-6NM8T-L4UQK-ZJAPW

CMD = akamai mpulse --json --api $(KEY)

TYPES = \
  ab-tests bandwidth browsers by-minute dimension-values geography histogram \
  metrics-by-dimension metric-per-page-load-time  \
  page-groups sessions-per-page-load-time summary timers-metrics

SAMPLES = $(addsuffix .json,$(addprefix sample-,$(TYPES)))

all: $(SAMPLES)

sample-%.json:
	$(CMD) --type $* > $@
