

package lint.gale

import org.scalatest._
import scala.xml.{XML,Elem,Node}


class NovelSpec extends FlatSpec with Matchers {

  ".identifier()" should "provide the PSMID" in {
    val novel = new Novel(NovelXML(identifier="1"))
    novel.identifier shouldEqual "1"
  }

  ".title()" should "provide the title" in {
    val novel = new Novel(NovelXML(title="Moby Dick"))
    novel.title shouldEqual "Moby Dick"
  }

  ".authorFirst()" should "provide the author's first name" in {
    val novel = new Novel(NovelXML(authorFirst="Herman"))
    novel.authorFirst shouldEqual "Herman"
  }

  ".authorLast()" should "provide the author's last name" in {
    val novel = new Novel(NovelXML(authorFirst="Melville"))
    novel.authorFirst shouldEqual "Melville"
  }

}


object NovelXML {

  def apply(
    identifier: String = "1",
    title: String = "Moby Dick",
    authorFirst: String = "Herman",
    authorLast: String = "Melville",
    year: Int = 1900
  ): Elem = {

//<?xml version="1.0" encoding="UTF-8"?>
//<!DOCTYPE book SYSTEM "amfcbook.dtd">
<book contentType="monograph" ID="{ identifier }" FAID="AMFCF0002" COLID="C00000">
	<bookInfo>
		<ocr>56.66</ocr>
    <PSMID>{ identifier }</PSMID>
		<assetID>WUQLKP724100933</assetID>
		<assetIDeTOC>LDWXMF531190421</assetIDeTOC>
		<dviCollectionID>AMFCC0001</dviCollectionID>
		<bibliographicID type="MARC">ocm05238011</bibliographicID>
		<reel>A-4</reel>
		<mcode>2YPR</mcode>
		<pubDate>
			<irregular>[1849]</irregular>
			<composed>[1849]</composed>
			<pubDateStart>{ year }0000</pubDateStart>
		</pubDate>
		<releaseDate>20160331</releaseDate>
		<sourceLibrary>
			<libraryName>Primary Source Media</libraryName>
			<libraryLocation>Meriden, CT, United States</libraryLocation>
		</sourceLibrary>
		<language ocr="English" primary="Y">English</language>
		<documentType>Monograph</documentType>
		<notes>Wright Bibliography Vol. I, 51</notes>
	</bookInfo>
	<citation>
		<authorGroup role="author">
			<author>
				<composed>McClure, David W.</composed>
        <first>{ authorFirst }</first>
				<middle>W.</middle>
        <last>{ authorLast }</last>
				<birthDate>1810</birthDate>
				<deathDate>1867</deathDate>
			</author>
		</authorGroup>
		<titleGroup>
			<fullTitle>{ title }</fullTitle>
			<displayTitle>{ title }</displayTitle>
		</titleGroup>
		<volumeGroup>
			<currentVolume>0</currentVolume>
			<Volume>0</Volume>
			<totalVolumes>0</totalVolumes>
		</volumeGroup>
		<imprint>
			<imprintFull>Philadelphia: Peterson, [1849]</imprintFull>
			<imprintPublisher>Peterson</imprintPublisher>
		</imprint>
		<collation>1 online resource 117 pages: illustrations</collation>
		<publicationPlace>
			<publicationPlaceCity>Philadelphia</publicationPlaceCity>
			<publicationPlaceState>Pennsylvania</publicationPlaceState>
			<publicationPlaceCountry>United States</publicationPlaceCountry>
			<publicationPlaceComposed>Philadelphia</publicationPlaceComposed>
		</publicationPlace>
		<totalPages>112</totalPages>
	</citation>
	<text>

		<page type="titlePage" firstPage="yes">
			<pageInfo>
				<pageID>00010</pageID>
				<assetID>IZPNRZ642169961</assetID>
				<ocrLanguage>English</ocrLanguage>
				<ocr>42.94</ocr>
				<imageLink pageIndicator="single" width="1842" height="2992" type="jpeg" colorimage="grayscale">AMFCF0002-C00000-B0000400-00010.jpg</imageLink>
			</pageInfo>
			<pageContent>
				<p>
					<wd pos="0,0,0,0">front</wd>
					<wd pos="0,0,0,0">matter</wd>
				</p>
			</pageContent>
		</page>

		<page type="bodyPage" firstPage="yes">
			<pageInfo>
				<pageID>00050</pageID>
				<assetID>YLWWEE906356237</assetID>
				<ocrLanguage>English</ocrLanguage>
				<sourcePage>11</sourcePage>
				<ocr>57.63</ocr>
				<imageLink pageIndicator="single" width="1896" height="2981" type="jpeg" colorimage="grayscale">AMFCF0002-C00000-B0000400-00050.jpg</imageLink>
			</pageInfo>
			<pageContent>
				<p>
					<wd pos="0,0,0,0">word</wd>
				</p>
			</pageContent>
		</page>

	</text>
</book>

  }

}
