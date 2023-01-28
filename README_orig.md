# txtuality

Code, data, and models to examine cultural production in its essential aspect as a txtuality. Rooted in the digital humanities, the package assists in corpus management, text analysis, and machine learning and AI. It is increasingly developing methods of synthesisizing knowledge, pooling data, and creating shared ontologies.

Just install:

```
pip install txtuality
```

Then:

```python
In [1]: from txtuality import Text

In [2]: texts = Text.find(author="Jane Austen")

In [3]: texts
Out[3]: 
TextList([Austen, LADY SUSAN IN THE WORKS OF JANE AUSTEN VOLUME VI M (1794) [_semantic_cohort/SC0112] <bh3hB>
          Austen, LADY SUSAN (1794) [_litlab/LL1792] <EILgo>
          Austen, THE WATSONS IN THE WORKS OF JANE AUSTEN VOLUME VI (1805) [_semantic_cohort/SC0272] <Kr7Ol>
          Austen, THE WATSONS (1805) [_litlab/LL1799] <Rhpzi>
          Austen, SENSEANDSENSIBILITY (1811) [_txtlab/EN_1811_Austen,Jane_SenseandSensibility_Novel] <2ORRZ>
          Austen, SENSE AND SENSIBILITY (1811) [_chadwyck/Nineteenth-Century_Fiction/ncf0204.08] <4hvU0>
          Austen, SENSE AND SENSIBILITY (1811) [_semantic_cohort/SC0355] <zTOJD>
          Austen, SENSE AND SENSIBILITY (1811) [_semantic_cohort/SC0356] <E1vVe>
          Austen, SENSE AND SENSIBILITY (1811) [_litlab/LL1798] <NPU8t>
          Austen, SENSE AND SENSIBILITY (1811) [_clmet/CLMET3_1_2_133] <WGBgY>
          Austen, PRIDE AND PREJUDICE (1813) [_semantic_cohort/SC0391] <SXBdD>
          Austen, PRIDE AND PREJUDICE (1813) [_litlab/LL1796] <jvB9W>
          Austen, PRIDE AND PREJUDICE (1813) [_clmet/CLMET3_1_2_134] <TmlJA>
          Austen, PRIDEANDPREJUDICE (1813) [_txtlab/EN_1813_Austen,Jane_PrideandPrejudice_Novel] <0sADH>
          Austen, PRIDE AND PREJUDICE (1813) [_chadwyck/Nineteenth-Century_Fiction/ncf0204.06] <aI7Lk>
          Austen, MANSFIELDPARK (1814) [_txtlab/EN_1814_Austen,Jane_MansfieldPark_Novel] <cwjSx>
          Austen, MANSFIELD PARK (1814) [_chadwyck/Nineteenth-Century_Fiction/ncf0204.03] <VHCpz>
          Austen, MANSFIELD PARK (1814) [_semantic_cohort/SC0403] <o0Jc1>
          Austen, MANSFIELD PARK (1814) [_litlab/LL1793] <8c5cG>
          Austen, MANSFIELD PARK (1814) [_semantic_cohort/SC0404] <l1qQI>
          Austen, EMMA (1816) [_chadwyck/Nineteenth-Century_Fiction/ncf0204.01] <63MVd>
          Austen, EMMA (1816) [_semantic_cohort/SC0434] <RCcEJ>
          Austen, EMMA (1816) [_litlab/LL1791] <xuf6s>
          Austen, EMMA (1816) [_semantic_cohort/SC0435] <bZtJC>
          Austen, SANDITON IN THE WORKS OF JANE AUSTEN VOLUME VI MIN (1817) [_semantic_cohort/SC0448] <ZbpOU>
          Austen, SANDITON (1817) [_litlab/LL1797] <zZQTz>
          Austen, NORTHANGER ABBEY AND PERSUASION (1818) [_semantic_cohort/SC0459] <nFlKk>
          Austen, LETTERS TO HER SISTER [_clmet/CLMET3_1_2_135] <ACUy6>
          Austen, NORTHANGER ABBEY (1818) [_chadwyck/Nineteenth-Century_Fiction/ncf0204.04] <WLYTU>
          Austen, NORTHANGER ABBEY (1818) [_litlab/LL1794] <jpzcf>
          Austen, NORTHANGER ABBEY (1818) [_semantic_cohort/SC0460] <Xqsaw>
          Austen, PERSUASION (1818) [_chadwyck/Nineteenth-Century_Fiction/ncf0204.05] <C96tI>
          Austen, PERSUASION (1818) [_litlab/LL1795] <cP7zC>
          Austen, PERSUASION (1818) [_semantic_cohort/SC0461] <6ghQJ>
          Austen, LADY SUSAN (1954) [_chadwyck/Nineteenth-Century_Fiction/ncf0204.02] <iviqB>
          Austen, SANDITON (1954) [_chadwyck/Nineteenth-Century_Fiction/ncf0204.07] <X7QKv>
          Austen, THE WATSONS (1954) [_chadwyck/Nineteenth-Century_Fiction/ncf0204.09] <YVvy0>])

In [4]: texts.match()
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████| 74/74 [00:11<00:00,  6.23it/s]
Out[4]: 
                                                 id_1                                             id_2  match_author  ...  match_sum  match_rel  match
71                                     _litlab/LL1792  _chadwyck/Nineteenth-Century_Fiction/ncf0204.02           1.0  ...        2.0        1.0   True
147                                    _litlab/LL1799  _chadwyck/Nineteenth-Century_Fiction/ncf0204.09           1.0  ...        2.0        1.0   True
191   _chadwyck/Nineteenth-Century_Fiction/ncf0204.08                          _semantic_cohort/SC0355           1.0  ...        2.0        1.0   True
192   _chadwyck/Nineteenth-Century_Fiction/ncf0204.08                          _semantic_cohort/SC0356           1.0  ...        2.0        1.0   True
193   _chadwyck/Nineteenth-Century_Fiction/ncf0204.08                                   _litlab/LL1798           1.0  ...        2.0        1.0   True
...                                               ...                                              ...           ...  ...        ...        ...    ...
1252                          _semantic_cohort/SC0461  _chadwyck/Nineteenth-Century_Fiction/ncf0204.05           1.0  ...        2.0        1.0   True
1253                          _semantic_cohort/SC0461                                   _litlab/LL1795           1.0  ...        2.0        1.0   True
1259  _chadwyck/Nineteenth-Century_Fiction/ncf0204.02                                   _litlab/LL1792           1.0  ...        2.0        1.0   True
1320  _chadwyck/Nineteenth-Century_Fiction/ncf0204.07                                   _litlab/LL1797           1.0  ...        2.0        1.0   True
1335  _chadwyck/Nineteenth-Century_Fiction/ncf0204.09                                   _litlab/LL1799           1.0  ...        2.0        1.0   True

[74 rows x 7 columns]

```

To be continued (porting functions from [LLTK](https://github.com/quadrismegistus/lltk)) ...