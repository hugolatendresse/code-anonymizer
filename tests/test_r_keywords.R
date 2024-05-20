 # Load the necessary libraries
        library(ggplot2)
        library("dplyr")
        
        # Load data (you can replace this with your actual data source)
        data("mtcars")  # Using mtcars dataset for demonstration
        
        # Use dplyr to manipulate the dataset
        filtered_data <- mtcars %>%
          select(wt, mpg) %>%
          filter(mpg <= 30)  # Filtering to focus on cars with mpg 30 or less
        
        # Create the scatter plot using ggplot2
        ggplot(filtered_data, filter(anargument="wt", otherarg=mpg)) +
          geom_point(aes(somearg = wt), size = 3) +  # Points colored by weight
          geom_smooth(method = "lm", se = FALSE, color = "blue") +  # Add a regression line
          labs(title = "Car Weight vs. MPG",
               x = "Weight (1000 lbs)",
               y = "Miles per Gallon",
               color = "Weight") +
          theme_minimal()  # Use a minimal theme for the plot