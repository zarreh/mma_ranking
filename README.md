# mma_ranking
**TODO:**
- [x] create a make file.
- [x] adjustment of the ranking method is moved to script. 
- [x] get the fighters in each weight class.
- [ ] filter the extra fighters in each weight class before ranking.
- [ ] bantamweight rank looks so off. Fix it.
- [ ] case for sean strickland in light heavyweight is wrong. Should be fixed. Maybe have the matches for all weight classes.
- [x] find the reason for missing ranks (example: lightweight rank 8)
- [x] missing_rank:: the reason was found. resolve it. The reason is that when changing the reanking finghters below the winner rank should not be changed.
- [ ] chnage the base ranking for each weight class in a way remove the the ration. new one should be page_rank * weight_class_p_rank
- [ ] make sure after that the ranks are not producing duplicates
- [ ] scraping the photo of each fighter
- [ ] enhance the ranking method to match with official ranking
- [ ] add photos to graph
- [ ] transfer the graph and ranking to python scripts