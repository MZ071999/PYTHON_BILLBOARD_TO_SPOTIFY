#Flow:

1. Asks user which year they want the songs from
2. Get request to https://www.billboard.com/charts/hot-100 + {user's input date}
3. Scrape the data and get all the title text
4. Make a call to spotify API
5. Create a new playlist containing all the songs

End-Result:
