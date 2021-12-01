---
title: Converting between 10– and 11– digit NDCs
description: 
date: "2017-02-24"
categories: [informatics]
tags: [NDC]
images: []
draft: false
---
## Background
National Drug Code, or NDC, numbers are 10-digit unique identifiers for human drug products marketed in the United States. Each NDC number comprises three sequential sections that describe different aspects of a drug product:

| Component | Length | Assigned&nbsp;by | Describes |
| --- | --- | --- | --- |
| Labeler&nbsp;code | 4–5&nbsp;digits | FDA | manufacturer, repackager, or relabeler of the product |
| Product&nbsp;code | 3–4&nbsp;digits | labeler | dosage characteristics of the drug (including strength and formulation) |
| Package&nbsp;code | 1–2&nbsp;digits | labeler | package type and size of the product |

You may have noticed that each of the different components of an NDC number is variable in length. NDCs did not always have this property, but as more labelers released products onto the market, the numbering space of the labeler code was deemed inadequately small and was expanded at the expense of the other two NDC components (in order to maintain a total of 10 digits). There are three length profiles for NDC numbers that result in a valid, 10-digit code: 4–4–2, 5–3–2, and 5–4–1. The history of NDCs is described in greater depth on the [RxTrace blog](https://www.rxtrace.com/2012/01/anatomy-of-the-national-drug-code.html/).

Normally, the three components of the NDC are delimited with dashes. For example, in the NDC 0781–1506–10, it's clear that 0781 is the labeler code, 1506 is the product code, and 10 is the package code. Often times, though, the dashes are lost, leaving an unseparated, 10-digit code. This is common during barcoding, in which an NDC number is encoded "bare" onto the outside of the product. As you can imagine, the fact that the three NDC components are variable in length often leads to ambiguity in situations where dashes are omitted or otherwise unavailable. For this reason, the 11-digit NDC in the 5–4–2 format is sometimes used as a standard to make it obvious which digits of the NDC correspond to which of the three NDC component sections.

## Converting From 10–digit to 11–digit NDC Numbers
If the full NDC number with dashes is known, the conversion from 10 to 11 digits is trivial. Simply add a leading zero to achieve a 5–4–2 format.

If the location of the dashes in the 10-digit NDC is not known, the conversion becomes much more difficult. Because there is no way to determine which section has been shortened, you must first convert the 10-digit NDC into each of the three possible formats (4–4–2, 5–3–2, and 5–4–1). Each of those 10-digit NDCs must then be compared to an NDC database like the FDA's [National Drug Code Directory](http://www.accessdata.fda.gov/scripts/cder/ndc/default.cfm) to determine which is the valid format. That format must then be expanded by the addition of a leading zero to produce a 5–4–2 format. In practice, this looks like this:

{{< figure src="/img/2017_02_24-converting_between_10_and_11_digit_NDCs/conversion-flowchart.png" caption="Figure 1. Conversion of an ambiguous 10-digit NDC to an 11-digit NDC" >}}

## Converting From 11–digit to 10–digit NDC Numbers
Occasionally, it may be necessary to convert from the 11-digit NDC back to a 10-digit NDC. The process for doing this is very similar to the one above, but in reverse. You need to first find the correct 10-digit format by removing a leading zero (if present) from each of the three NDC sections and comparing the resulting 10-digit numbers to an NDC database. Once you determine the correct format, you just need to add the dashes back to their original positions.

## NDC Conversion Tool
To make life a little easier, you can type a 10– or 11–digit NDC number into the box below and it will automatically convert it to the opposite type for you.

<script> function clearConverter() {
			document.getElementById("ndcIn").style.backgroundColor = "";
			document.getElementById("resultNDC").innerHTML = "";
		}
		
		function updateMode() {
			var mode = document.querySelector('input[name="mode"]:checked').value;
			if (mode == "10to11") {
				document.getElementById("inputLen").innerHTML = "10";
				document.getElementById("outputLen").innerHTML = "11";
				document.getElementById("ndcIn").maxLength = 10;
			}
			else if (mode == "11to10") {
				document.getElementById("inputLen").innerHTML = "11";
				document.getElementById("outputLen").innerHTML = "10";
				document.getElementById("ndcIn").maxLength = 11;
			}
			document.getElementById("ndcIn").value = "";
			clearConverter();
		}
		
		var resultNDC = -1;
		function convertNDC() {
			var mode = document.querySelector('input[name="mode"]:checked').value;
			var inputLen;
			if (mode == "10to11") { inputLen = 10; }
			else if (mode == "11to10") { inputLen = 11; }
			if (document.getElementById("ndcIn").value.length == inputLen) {
				document.getElementById("ndcIn").style.backgroundColor = "#FFFFDD";
				var inputNDC = document.getElementById("ndcIn").value;
				resultNDC = -1;
				if (mode == "10to11") {
					var preliminary = new Array();
					preliminary[0] = "0".concat(inputNDC); // 4-4-2 input
					preliminary[1] = inputNDC.substring(0,5).concat("0").concat(inputNDC.substring(5)); // 5-3-2 input
					preliminary[2] = inputNDC.substring(0,9).concat("0").concat(inputNDC.substring(9)); // 5-4-1 input
					for (var i = 0; i < 3; i++) {
						validateNDC(preliminary[i]);
					}
				}
				if (mode == "11to10") {
					var crumbs = new Array();
					var preliminary = new Array();
					crumbs[0] = inputNDC.substring(0,5).concat("-");
					crumbs[1] = inputNDC.substring(5,9).concat("-");
					crumbs[2] = inputNDC.substring(9);
					if (crumbs[0].substring(0,1) == "0") { preliminary.push(crumbs[0].substring(1).concat(crumbs[1]).concat(crumbs[2])) }
					if (crumbs[1].substring(0,1) == "0") { preliminary.push(crumbs[0].concat(crumbs[1].substring(1)).concat(crumbs[2])) }
					if (crumbs[2].substring(0,1) == "0") { preliminary.push(crumbs[0].concat(crumbs[1]).concat(crumbs[2].substring(1))) }
					for (var i = 0; i < 3; i++) {
						validateNDC(preliminary[i]);
					}
				}
				if (resultNDC != -1) {
					document.getElementById("resultNDC").innerHTML = resultNDC;
					document.getElementById("ndcIn").style.backgroundColor = "#DDFFDD";
				}
				else {
					document.getElementById("resultNDC").innerHTML = "Invalid NDC";
					document.getElementById("ndcIn").style.backgroundColor = "#FFDDDD";
				}
			}
			else {
				clearConverter();
				document.getElementById("ndcIn").value = document.getElementById("ndcIn").value.replace(/\D/g,'');
			}
		}
		function validateNDC(inputNDC) {
			var rxNorm = new XMLHttpRequest();
			var outputNDC = -1;
			rxNorm.onreadystatechange = function() {
				if (rxNorm.readyState == 4 && rxNorm.status == 200) {
					var xmlData = rxNorm.responseXML;
					if (xmlData.getElementsByTagName("status")[0].innerHTML.toLowerCase() == "active") { resultNDC = inputNDC; }
				}
			};
			rxNorm.open("GET", "https://rxnav.nlm.nih.gov/REST/ndcstatus?ndc=".concat(inputNDC), false);
			rxNorm.send();
		} </script>
<form id="ndcConverter"><table><tr><td>Mode selector</td><td><input type="radio" name="mode" value="10to11" checked="checked" onclick="updateMode()"> 10&rarr;11<br><input type="radio" name="mode" value="11to10" onclick="updateMode()">11&rarr;10</td></tr><tr><td><span id="inputLen">10</span>-digit NDC</td><td><input type="text" id="ndcIn" size="13" maxlength="10" name="NDC" onkeyup="convertNDC()"></td></tr><tr><td><span id="outputLen">11</span>-digit NDC</td><td><span id="resultNDC">&nbsp;</span></td></tr></table></form>
 
## Conclusion
The 10-digit NDC format can lead to ambiguity if dashes are not present, like in the case of scanned barcode data. The 11-digit NDC format removes that ambiguity, but the conversion between formats can be difficult and requires a database of known NDCs numbers.