.PHONY: all clean zip install

all: zip

zip: fhighlight.ankiaddon

pygments.tgz:
	curl -L -o pygments.tgz https://github.com/pygments/pygments/archive/refs/tags/2.10.0.tar.gz

src/vendor/pygments:
	( mkdir -p src/vendor; cd src/vendor; tar xf ../../pygments.tgz --strip-components=1 pygments-2.10.0/pygments )

fhighlight.ankiaddon: $(shell find src -type f ) src/vendor/pygments
	rm -f $@
	rm -rf src/__pycache__
	( cd src/; zip -r ../$@ * )

# install in test profile
install: ankiprofile/addons21/fhighlight

ankiprofile/addons21/fhighlight: $(shell find src -type f ) src/vendor/pygments
	rm -rf src/__pycache__
	cp -r src/. ankiprofile/addons21/fhighlight

clean:
	rm -f *.pyc
	rm -f src/*.pyc
	rm -f src/__pycache__
	rm -f fhighlight.ankiaddon
