from clarity_ext.extensions import GeneralExtension
from genologics.config import BASEURI, USERNAME, PASSWORD
from genologics.lims import Lims
import getopt
import re
import sys


def my_print(print_str):
    print(print_str)

def post_xml():
    xml = """<?xml version='1.0' encoding='UTF-8'?>
<rt:routing xmlns:rt='http://genologics.com/ri/routing'>
	    <unassign stage-uri='https://lims-staging.snpseq.medsci.uu.se/api/v2/configuration/workflows/210/stages/537'>
		    <artifact uri='https://lims-staging.snpseq.medsci.uu.se/api/v2/artifacts/2-11222'/>
	    </unassign>
	    <assign stage-uri='https://lims-staging.snpseq.medsci.uu.se/api/v2/configuration/workflows/210/stages/536'>
		    <artifact uri='https://lims-staging.snpseq.medsci.uu.se/api/v2/artifacts/2-11222'/>
	    </assign>
</rt:routing>
"""
    uri = "https://lims-staging.snpseq.medsci.uu.se/api/v2/route/artifacts/"
    lims = Lims(BASEURI, USERNAME, PASSWORD)
    lims.post(uri, data=xml)
    print("REST post is executed!")

def main():

	global api

	pURI = ""
	username = ""
	password = ""
	status = ""
	message = ""
	hostname = ""

   	opts, extraparams = getopt.getopt(sys.argv[1:], "l:u:p:s:m:")

	for o,p in opts:
		if o == '-l':
			pURI = p
			hostname = re.sub('(.*)(\/api/.*)', '\\1', pURI)

		elif o == '-u':
			username = p
		elif o == '-p':
			password = p
		elif o == '-s':
			status = p
		elif o == '-m':
			message = p

        post_xml()


if __name__ == "__main__":
    main()

