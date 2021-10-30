.PHONY: all clean zip

all: zip

zip: fhighlight.ankiaddon

fhighlight.ankiaddon: src/* pygments.tgz
	rm -f $@
	rm -f src/meta.json
	rm -rf src/__pycache__
	( mkdir src/vendor; cd src/vendor; tar xf ../../pygments.tgz --strip-components=1 pygments-2.10.0/pygments )
	( cd src/; zip -r ../$@ * )

pygments.tgz:
	curl -L -o pygments.tgz https://github.com/pygments/pygments/archive/refs/tags/2.10.0.tar.gz

clean:
	rm -f *.pyc
	rm -f src/*.pyc
	rm -f src/__pycache__
	rm -f fhighlight.ankiaddon
