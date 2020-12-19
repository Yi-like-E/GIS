# Description: Using twitter API to create a tweet crawler to get a stream of tweets with the keyword "friday" and creat a map with red dot showing where the tweet was being tweeted.

#import system modules
import tweepy
import sys
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Get access and key from authentication class
consumer_key = "srL0cdVJt2cI30pcgMHbtxWJI"
consumer_secret = "LcxebddePMKMmCqTb8wqVRJ2lWLWArAKKBFZdbZAgqlfQxfjsc"
access_token = "1053717745-f6PmZwXMlC0SZmMW38STtCRF3fGtOyyiH8ZLmFi"
access_token_secret = "Qq8EyhKC6G5umouxeTxhiQAJAcppswk1MO6t1Bzz4yNVq"



#Create a listener to fetch live stream tweets with coordinates and chosen keyword
class TorontoStreamListener(tweepy.StreamListener):
    """ A listener handles tweets are the received from the stream. This is a listener to print out received tweets."""
    def __init__(self):
        super().__init__()
        self.tweet_counter = 0
        self.text_position = self.get_axis_limits(ax)                               # set textbox position
        self.tweet_counter_text = ax.text(self.text_position[0],                    # x position
                                          self.text_position[1],                    # y position
                                          "Tweets : " + str(self.tweet_counter),    # text
                                          fontsize=9,                               # fontsize
                                          ha="center", va="center",                 # position of text in the box
                                          color=(0.30, 0.34, 0.42),                 # textcolor
                                          bbox=dict(                                # fancybox
                                              boxstyle="square,pad=0.3",            # square with padding
                                              ec=(0.85, 0.87, 0.91),                # inner color
                                              fc=(0.93, 0.94, 0.96)                 # border color
                                          ))
    
    def on_status(self, status):
        if "friday" in status.text:                   # Make sure the tweets have the keyword "friday"
            if status.coordinates is not None:        # Make sure the tweets have coordinates to be mapped
                self.get_tweet(status)                # Get the tweets that have both keyword and coordinates
                self.tweet_counter += 1               # Increment the counter while collecting tweets
                self.tweet_counter_text.set_text("Tweets : " + str(self.tweet_counter)) # Update counts     
                print ("Tweet found: "+ status.text)  # Print the tweets that have both the keyword and coordinates                     
        if self.tweet_counter == 20:                  # Set a threshold of tweets to be mapped
            print('20 tweets collected')              # Print "20 tweets collected" when the threshold is met. 
            plt.show()
            return False
        else:
            return True


    def on_error(self, status_code):
        print (sys.stderr, "Encountered error with status code:", status_code)  # When error occurs, display a message with status code
        return True     # Continue trying - do not end the stream
    
    @staticmethod
    def get_axis_limits(axes, scale_x=0.75, scale_y=0.95):      # Return the axis view limits and set the scale to place the counter
        return axes.get_xlim()[0] * scale_x, (axes.get_ylim()[0] * scale_y)

    @staticmethod
    def get_tweet(tweet):
        x, y = tweet.coordinates['coordinates']  # Get coordinates from the tweet
        plt.plot(x, y, 'ro', markersize=3)       # Plot the red dot on the map
        plt.pause(0.01)                          # To update the map




# Define the map
if __name__ == '__main__':
    NorthAmerica_extent = [-130.12753572,-64.3150314285,24.3607274755,50.8542437648]    # Central United States coordinates 
    stamen_terrain = cimgt.Stamen('terrain')        # Create a Stamen terrain background instance
    fig = plt.figure(figsize=(9,5), dpi=150)        # Define size and dpi of the map
    ax = plt.axes(projection = ccrs.PlateCarree())  # Create a GeoAxes in the tile's projection
    ax.stock_img()                                  # Put a sea rendering background image 
    ax.gridlines()                                  # Add grid lines
    ax.set_extent(NorthAmerica_extent, crs=ccrs.PlateCarree())          # Limit the extent of the map to a small longitude/latitude range
    ax.add_image(stamen_terrain, 6)                                     # Add the Stamen data at zoom level 6
    plt.title("Mapping livestream tweets in Central United States")     # Set a title


    # Authentication 
    auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    # Construct the API instance
    api = tweepy.API(auth)
    print ("Successfully logged in as " + api.me().name + ".")      # Once logged in, print out logged in as _____ .
    streamListener = TorontoStreamListener()
    streamapi = tweepy.Stream(auth=api.auth, listener=streamListener)   # Our listener
    streamapi.filter(track=["friday"],locations=[-130.12753572,24.3607274755,-64.3150314285,50.8542437648]) # Fetch tweets with both the keyword and coordinates
