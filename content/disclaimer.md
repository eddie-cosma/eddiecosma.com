---
title: Disclaimer for @OHVaxStats
date: "2021-12-06"
categories: []
tags: []
images: []
draft: false
---
## General

The Twitter post content (the "Content") provided by this account is for educational purposes only. It is not intended to substitute for professional medical advice, diagnosis, or treatment. Effort is made to ensure data accuracy and reliability, however no guarantee can be made to this effect.

THE CONTENT IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE CONTENT OR THE USE OR OTHER DEALINGS IN THE CONTENT.

## Herd immunity estimate

The bot posting to [@OHVaxStats](https://twitter.com/OHVaxStats) uses a simplified model to attempt to estimate a date at which herd immunity will be reached based on current vaccination trends. This model makes a number of assumptions that must be carefully considered.

- An r<sub>0</sub> value of 6.5 is used. This is based on reports from medical literature and the media in the context of the now-predominant delta variant.<sup>1,2</sup>
- The use of r<sub>0</sub> is inherently flawed because it assumes a completely susceptible population.<sup>3</sup> In other words, it does not account for individuals becoming less susceptible due to previous infection or vaccination. Previous estimates of r<sub>0</sub> also do not account for changes in transmissibility due to emerging vaccine variants.
- The model currently assumes that a complete vaccination with a booster confers 93% protection against COVID-19, complete vaccination without a booster confers 48% protection, and a single dose confers 10% protection.<sup>4,5</sup> The efficacy of a single dose has not been studied in the context of the predominant delta variant, so this number is a guess. The model does not take into account the time it takes for immunity to be reached after vaccination and does not account for immunity waning over time.
- The model calculates the rate at which people are being vaccinated and extrapolates this into the future assuming a linear vaccination rate. In reality, vaccination rates may be nonlinear or otherwise fluctuate based on a number of factors including product availability, emergency use authorization of novel vaccines, and prevailing attitudes towards vaccination.
- Because data is analyzed in aggregate for the state of Ohio, the assumption is that vaccination pravalence and incidence are homogenous across the state. This is not the case. Because of differences in geographic vaccination rates, many areas may see herd immunity slower than predicted.

Because of these limitations, herd immunity predictions should be viewed with a high degree of skepticism. They constitute a best-effort attempt at predicting when herd immunity will be reached, but with a high degree of variability that is itself difficult to quantify.

## References

1. Kang M, Xin H, Yuan J, et al. Transmission Dynamics and Epidemiological Characteristics of Delta Variant Infections in China. *Epidemiology*. 2021.
2. https://www.npr.org/sections/goatsandsoda/2021/08/11/1026190062/covid-delta-variant-transmission-cdc-chickenpox
3. https://coronavirus.ohio.gov/wps/portal/gov/covid-19/resources/news-releases-news-you-can-use/basic-reproduction-number-pop-up-sites
4. Delamater PL, Street EJ, Leslie TF, Yang YT, Jacobsen KH. Complexity of the Basic Reproduction Number (R<sub>0</sub>). *Emerging Infectious Diseases*. 2019;25(1):1–4.
5. Tartof SY, Slezak JM, Fischer H, et al. Effectiveness of mRNA BNT162b2 COVID-19 vaccine up to 6 months in a large integrated health system in the USA: a retrospective cohort study. *The Lancet*. Published online October 2021:S0140673621021838.