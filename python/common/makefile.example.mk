GPSOURCE = $(REPOROOT)/pleurotus

ifeq ($(COMMONSOURCE),)
COMMONSOURCE = $(REPOROOT)/muttley
endif

log.yml: $(GPSOURCE)/common/gp.log.yml
	cp $< $@

common:
	mkdir -p $@

common/__init__.py common/logger.py: common/%: $(COMMONSOURCE)/python/lib/common/%
	cp $< $@

update-common: common log.yml common/logger.py
