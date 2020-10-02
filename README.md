# tidypodcatch – Python3 Podcast archiver

tidypodcatch is a simple podcast archiver, written in Python3.

## Project Goals

* Simple install, minimal dependencies
* Cron-able
* Logical folder & filename structure of the downloaded files

## Installation

* Install Python3.
* Install feedparser library
* Download the py file. 
* Create a configuration xml file

## Execution
    tidypodcatch.py <xml file>
The file _meta.txt_ is created by the script. Every time a podcast is downloaded the RSS metadata for that episode is appended to the end. A separate _meta.txt_ is created in each directory podcasts are downloaded in to.

The script will download any episode where a file of the name does not already exist and will skip any episode where is does.

## Configuration
tidypodcatch uses an xml file to configure podcast archiving.
* Each Podcast requires a <Podcast> block.
* _&lt;Title&gt;_ is not used by the script is and is provided as a readability aide.
* _&lt;Path&gt;_ is the folder to save the files. Recommend a separate folder for each RSS feed
* The filename is defined using the list of _&lt;atom&gt;_ elements in the _&lt;FilenameFormat&gt;_ block concatinated with the spacer " - ". An atom can be any of the metadata fields in the RSS feed. Date can also be used which will return publication date in the format YYYY-MM-DD. 
  *  Example: _&lt;atom&gt;itunes_season&lt;/atom&gt;_ _&lt;atom&gt;itunes_episode&lt;/atom&gt;_ _&lt;atom&gt;title&lt;/atom&gt;_ will result in filenames along the line of _0001 - 0001 - The podcast episode titles_

## XML Template
```<?xml version="1.0" standalone="yes"?>
<tpc>
<Podcast>
  <Title></Title>
  <RSS></RSS>
  <Path></Path>
  <FilenameFormat>
    <atom></atom>
    <atom></atom>
    ...
    <atom></atom>
  </FilenameFormat>
</Podcast>
```
