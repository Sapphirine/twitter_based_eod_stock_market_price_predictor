#!/usr/bin/env python
import json

def getDateAndText( filename ):
    ''' Method for prasing a file of entries to only include the "created_at" and "text" '''
    parsedEntries = []
    with open( filename ) as jData:
        for line in jData:
            jLine = json.loads( line )
            if u'user' in jLine:
                tempDict = {}
                tempDict[ u'created_at' ] = jLine[ u'created_at' ]
                tempDict[ u'text' ] = jLine[ u'text' ]
                parsedEntries.append( tempDict )
            else:
                continue
    jData.close()
    return parsedEntries

def writeOutputJSON( companyName, listOfEntries) :
    ''' Method for taking in a list of entries and writing an output json
        file containing those entries '''
    strListOfEntries = [ str( entry ) for entry in listOfEntries ]
    with open( companyName+'_parsed'+'.json', 'a+' ) as en:
        en.write( '\n'.join( strListOfEntries ) )
    en.close()

if __name__ == "__main__":
    import sys
    parsedEntries = getEnglishEntries( sys.argv[ 1 ] ) 
    writeOutputJSON( sys.argv[ 2 ], parsedEntries )
