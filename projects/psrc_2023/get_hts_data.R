library(psrcelmer)
library(tidyverse)

incl_years <- c("2023")
HTS_data_dir <- "C:/Joanne_PSRC/travel_models/travel-diary-survey-tools/projects/psrc_2023/data"

hh <- get_table(schema = 'HHSurvey', tbl_name = 'v_households_labels') %>%
  filter(survey_year %in% incl_years) %>%
  rename(hh_id = household_id)
person <- get_table(schema = 'HHSurvey', tbl_name = 'v_persons_labels') %>%
  filter(survey_year %in% incl_years) %>%
  rename(hh_id = household_id)
day <- get_table(schema = 'HHSurvey', tbl_name = 'v_days_labels') %>%
  filter(survey_year %in% incl_years) %>%
  rename(hh_id = household_id)
trip <- get_table(schema = 'HHSurvey', tbl_name = 'v_trips_labels') %>%
  filter(survey_year %in% incl_years) %>%
  rename(hh_id = household_id)

write_csv(hh, file.path(HTS_data_dir,"v_households_labels.csv"))
write_csv(person, file.path(HTS_data_dir,"v_persons_labels.csv"))
write_csv(day, file.path(HTS_data_dir,"v_days_labels.csv"))

trip2 <- trip %>% select(-c("dest_x_coord","dest_y_coord","dest_tract20",
                            "origin_x_coord","origin_y_coord","origin_tract20",
                            "dwell_mins",
                            "arrival_time_hour","arrival_time_minute","arrival_time_second",
                            "depart_time_hour","depart_time_minute","depart_time_second",
                            "distance_meters","distance_miles","duration_minutes",
                            "duration_seconds","speed_mph"))
write_csv(trip2, file.path(HTS_data_dir,"v_trips_labels.csv"))
