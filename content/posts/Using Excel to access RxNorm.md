---
title: Using Excel to access RxNorm
description: 
date: "2017-01-08"
categories: [informatics]
tags: [RxNorm, Excel]
images: []
draft: false
---
## Background
Let's say you work in an institutional pharmacy that performs a physical inventory every December. This year, you discover there's a large discrepancy between the value of your current medication stock compared to the value of last year's stock. Apparently, some of the data on the handheld computers you use to perform inventory became corrupted before everything could be compiled into one large Excel file. Now you're missing a few hundred line items, the end of the year is coming up, and Accounting is breathing down your neck. You don't know what to do because there's no real pattern to this missing drug data, but one thing you do still have is the Excel file from last year's inventory.

Maybe you could compare last year's data to this year's data and see what's missing. It's a great idea in theory, but you notice that the columns containing the names of the drug formulations have minor differences because of the way your wholesaler's listings changed over the course of the year. No amount of Excel wizardry is going to let you find the differences between the column items meaningfully, and there are thousands of line items, so comparing them by hand is out. You do find NDC numbers associated with each line item in both documents, but those aren't directly comparable either because of the frequency at which you switch between product manufacturers. Now what?

{{< figure src="/img/2017_01_08-using_excel_to_access_rxnorm/inventory.png" caption="Figure 1. Example of nonstandard drug naming with NDC numbers" >}}

## RxNorm and Standard Drug Terminology
One of the problems with pharmaceuticals is that there are a plethora of ways to represent a drug or group of drugs semantically. The ambiguity between divalproex, divalproex ER, and divalproex DR constitutes a single example of the challenges that result from managing a medication inventory. In order to help make it easier to communicate exactly what drug or group of drugs is being referenced, the FDA created a database called [RxNorm](https://www.nlm.nih.gov/research/umls/rxnorm/index.html), which touts itself as being a normalized drug naming system. Each drug "concept" is stored in the database under a numerical RXCUI, or RxNorm concept unique identifier, and refers to a specific string of text used to identify a drug or drugs. Some examples of drug concepts include:

-   "Naproxen"
-   "Naproxen 250 MG"
-   "Naproxen Oral Tablet"

One of the core features of RxNorm is an API, or application program interface, which makes it easy to build software applications around the database. Looking at the [API documentation](https://mor.nlm.nih.gov/download/rxnav/RxNormAPIs.html), you notice that there's a function that can be used to [convert NDC numbers into RXCUI values](https://mor.nlm.nih.gov/download/rxnav/RxNormAPIs.html#uLink=RxNorm_REST_findRxcuiById). More on this later.

To build on the scenario above: you deduce that one way to compare the inventory list from last year to that from this year is to convert the NDC from every line item into a standardized drug name and then compare the results. This way, it doesn't matter if the NDC numbers of your inventory on-hand changed from year to year. It also doesn't matter that your wholesaler changed their drug nomenclature because you can now ignore it altogether.

## Converting an NDC to an RXCUI
Using the [`rxcui`](https://mor.nlm.nih.gov/download/rxnav/RxNormAPIs.html#uLink=RxNorm_REST_findRxcuiById) resource from the RxNorm API, you can convert an NDC number to an RXCUI. This resource is located at `https://rxnav.nlm.nih.gov/REST/rxcui` and takes a number of arguments. Using `?idtype=NDC` specifies that you want to pass an NDC number to `?id=`. Mercifully, the API will accept any 10- or 11-digit NDC number, so you do not have to convert your NDC numbers between formats (do note that 10-digit numbers must include dashes; for more information, see my article on [NDC conversion](/posts/converting-between-10-and-11-digit-ndcs/). Let's use the NDC 0781–1506–10 as an example. Putting this all together gives us the following address:

```
https://rxnav.nlm.nih.gov/REST/rxcui?idtype=NDC&id=0781-1506-10
```

If you open that location in a web browser, you're greeted with an XML file containing an RXCUI (as `<rxnormId>`) for our example NDC:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<rxnormdata>
    <idGroup>
        <idType>NDC</idType>
        <id>0781-1506-10</id>
        <rxnormId>197381</rxnormId>
    </idGroup>
</rxnormdata>
```

## Converting Between RxNorm Term Types
At this point, it's worth taking a moment to mention that RxNorm uses [term types](https://www.nlm.nih.gov/research/umls/rxnorm/docs/2015/appendix5.html) (TTYs) to describe the level of complexity included in an RXCUI term, and there are different RXCUIs that may apply to a single product depending on the desired level of specificity. For example, a fluoxetine capsule may be linked to an RxNorm concept of "fluoxetine" (TTY = IN ["ingredient"]) at the same time it is linked to an RxNorm concept of "fluoxetine oral product" (TTY = SCDG ["semantic clinical dose form group"]). Different RXCUIs with different term types that all refer to a single product are linked with a complex relationship model that's built in to the RxNorm database. Using the `rxcui` API resource to look up an RXCUI can be unpredictable because it assumes a TTY. For this reason, it may be necessary to convert between term types if you're performing comparison operations like in our hypothetical scenario.

In order to convert between term types, we can again use the [`rxcui`](https://mor.nlm.nih.gov/download/rxnav/RxNormAPIs.html#uLink=RxNorm_REST_getRelatedByType) API resource with the following URL structure:

```
https://rxnav.nlm.nih.gov/REST/rxcui/{RXCUI}/related?tty={TTY Code}
```

For the purpose of our example, we want to use the SCD ("semantic clinical drug") TTY. Inserting our previous RXCUI and the TTY code into the URL gives us:

```
https://rxnav.nlm.nih.gov/REST/rxcui/197381/related?tty=SCD
```

Again, visiting this address yields an XML file with a new RXCUI (as `<rxnormId>`) and the coveted standardized terminology string (as `<name>`):

```xml
<rxnormdata>
    <relatedGroup>
        <rxcui>197381</rxcui>
        <termType>SCD</termType>
        <conceptGroup>
            <tty>SCD</tty>
            <conceptProperties>
                <rxcui>197381</rxcui>
                <name>Atenolol 50 MG Oral Tablet</name>
                <synonym/>
                <tty>SCD</tty>
                <language>ENG</language>
                <suppress>N</suppress>
                <umlscui>C0687940</umlscui>
            </conceptProperties>
        </conceptGroup>
    </relatedGroup>
</rxnormdata>
```

## Accessing RxNorm with Excel
So this is all well and good, but what we really want is to take these XML files, parse the important data, and enter them into an Excel spreadsheet. Doing this manually, or even programmatically, could take a considerable amount of time. Luckily, the newer versions of Excel has a few functions that can automatically access the XML files corresponding to each of our RxNorm queries and parse them. Note that this will only work in Excel 2013 or later for Windows (i.e., this will not work on macOS).

The first important function is `WEBSERVICE(url)`, which accepts a single URL parameter as a string and returns the contents of the file located at that URL. An NDC in cell A1 can be passed to RxNorm with the formula:

```
=WEBSERVICE("https://rxnav.nlm.nih.gov/REST/rxcui?idtype=NDC&id=" & A1)
```

The problem is that this would insert the entire contents of the XML file into your Excel file. The `=FILTERXML(xml, xpath)` function can be used to further whittle down the data to a usable RXCUI. The previous `WEBSERVICE` function can be passed as the `xml` parameter, and the path of the `<rxnormId>` tag in the file can be passed as an XPath string (More information on XPath can be found on the [W3Schools website](http://www.w3schools.com/xml/xpath_intro.asp)). This ends up looking like this:

```
=FILTERXML(WEBSERVICE("https://rxnav.nlm.nih.gov/REST/rxcui?idtype=NDC&id=" & A1),
	"//rxnormID")
```

Following our scenario above, the resulting numerical RXCUI can be stored in a helper column, B, in Excel. A third column could use the following function to return a normalized drug name:

```
=FILTERXML(WEBSERVICE("https://rxnav.nlm.nih.gov/REST/rxcui/"
	& B1 & "/related?tty=SCD"), "//name[1]")
```

{{< figure src="/img/2017_01_08-using_excel_to_access_rxnorm/inventory_standardized.png" caption="Figure 2. Example of standardized drug naming" >}}

At this point, we have the data we need to compare last year's inventory to this year's, which can be done trivially. Don't forget that you can extend these formulas down a dataset by double clicking the green box on the bottom-right corner of a selected cell. Do note that when doing this with thousands of rows of data, each row requires a separate set of web queries and so Excel can take some time to populate the cells. You must be patient. I believe that Excel will exceed the [RxNorm maximum of 20 requests per second](https://mor.nlm.nih.gov/download/rxnav/TermOfService.html), but when using a dataset of around 2,000 rows, I did not run into any problems. Be conscious and try to limit the number of times you perform large queries on the database.

## Conclusion
RxNorm is a powerful tool that can be integrated into Excel-based solutions for a wide variety of problems that occur in a typical pharmacy. The examples shown here of RxNorm functionality really just scratch the surface. I encourage you to explore the rest of the API on the [RxNorm website](https://mor.nlm.nih.gov/download/rxnav/TermOfService.html) and consider what other problems you can use it to solve by combining it with the data-handling capabilities and ease-of-use of Excel.