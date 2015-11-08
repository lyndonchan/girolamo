# girolamo
<img align="right" src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/db/Caravaggio_-_San_Gerolamo.jpg/320px-Caravaggio_-_San_Gerolamo.jpg">

A simple-to-use script that retrieves scriptural quotations from various Catholic translations of the Bible. 

Currently, numerous resources exist online to retrieve passages from Protestant translations of the Bible, but equivalent resources are not readily available for the Catholic bible. Currently, the online user of the Catholic bible is forced to go directly to the full text source of the Bible and manually copy-paste the passage that they want, and then manually remove all the extraneous formatting (e.g. footnote and verse numbering) from the text.

Girolamo is the Italian name of St. Jerome, the patron saint of Bible scholars, archivists, and translators. Born in 4th century Illyria, he wrote extensively and is best known today for translating the entire Bible into the Latin Vulgate.

## Features
Supported as of Girolamo 1.0:
* English
 * New American Bible (NAB) [Source: Vatican website]
* Chinese (Traditional)
 * Studium Biblicum Bible / 思高聖經(SB) [Source: John Duns Scotus Bible Reading Promotion Center]

## Dependencies
* Python 2.7 (https://www.python.org/downloads/)
* BeautifulSoup 4 ("pip install BeautifulSoup4")

## Usage
### Help
```
python girolamo.py --help
usage: girolamo.py [-h] [-l LANGUAGE] [-q QUERY]

Welcome to Girolamo 1.0! Girolamo will read in a scriptural reference and
retrieve it for you in a text file. English text is from the Vatican website's
New American Bible, Chinese text is from the John Duns Scotus Bible Reading
Promotion Center's Studium Biblicum translation

optional arguments:
  -h, --help            show this help message and exit
  -l LANGUAGE, --language LANGUAGE
                        "E" for English, "C" for Chinese, "B" for English and
                        Chinese
  -q QUERY, --query QUERY
                        Type in the Book, Chapter, and Verse range of your
                        Scriptural quotation without spaces, e.g. John3:14-17
```
### Example usecase
Console command
```
python girolamo.py -l B -q John3:14-17
```
Sample text output (English)
```
And just as Moses lifted up the serpent in the desert, so must the Son of Man be lifted up, so that everyone who believes in him may have eternal life." For God so loved the world that he gave his only Son, so that everyone who believes in him might not perish but might have eternal life. For God did not send his Son into the world to condemn the world, but that the world might be saved through him.
```
Sample text output (Chinese)
```
正如梅瑟曾在曠野裡高舉了蛇，人子也應照樣被舉起來，使凡信的人，在他內得永生。」天主竟這樣愛了世界，甚至賜下了自己的獨生子，使凡信他的人不至喪亡，反而獲得永生，因為天主沒有派遣子到世界上來審判世界，而是為叫世界藉著他而獲救。
```
