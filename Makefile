DOMAIN_NAME = Minesweeptk
TARGETS = locale/it/LC_MESSAGES/$(DOMAIN_NAME).mo \
          locale/en/LC_MESSAGES/$(DOMAIN_NAME).mo \
          locale/ja/LC_MESSAGES/$(DOMAIN_NAME).mo

.PHONY : all
all : $(TARGETS)


locale/it/LC_MESSAGES/$(DOMAIN_NAME).mo : it.po
	mkdir -p $$(dirname $@)
	msgfmt $< -o $@
	
locale/en/LC_MESSAGES/$(DOMAIN_NAME).mo : en.po
	mkdir -p $$(dirname $@)
	msgfmt $< -o $@

locale/ja/LC_MESSAGES/$(DOMAIN_NAME).mo : ja.po
	mkdir -p $$(dirname $@)
	msgfmt $< -o $@

.PHONY : clean
clean :
	-rm $(TARGETS)

