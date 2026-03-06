library(psrcelmer)
library(tidyverse)

incl_years <- c("2023")
HTS_data_dir <- "C:/Joanne_PSRC/travel_models/travel-diary-survey-tools/projects/psrc_2023/data"

hh <- get_table(schema = 'HHSurvey', tbl_name = 'v_households_labels') %>%
  filter(survey_year %in% incl_years) %>%
  rename(hh_id = household_id) %>%
  select(hh_id,
         hhincome_detailed,hhincome_followup,hhincome_broad,
         rent_own,res_type,vehicle_count,numworkers,hhsize,
         home_lat, home_lng,
         hh_weight) %>%
  mutate(home_in_region = 1)


person <- get_table(schema = 'HHSurvey', tbl_name = 'v_persons_labels') %>%
  filter(survey_year %in% incl_years) %>%
  rename(hh_id = household_id) %>%
  # reassign school in region column
  mutate(
    school_in_region = case_when(
     is.na(school_loc_lat)~NA,
     school_county %in% c("King County","Kitsap County","Pierce County","Snohomish County")~ "Yes", 
     TRUE~ "No")
    ) %>%
  select(person_id,hh_id,pernum,
         age,education,employment,gender,industry,workplace,relationship,telecommute_freq,school_freq,schooltype,
         adult_student,commute_freq,work_mode,commute_subsidy_1,commute_subsidy_3,
         work_lng,work_lat,school_loc_lng,school_loc_lat,school_in_region,
         person_weight)


day <- get_table(schema = 'HHSurvey', tbl_name = 'v_days_labels') %>%
  filter(survey_year %in% incl_years) %>%
  rename(hh_id = household_id)
trip <- get_table(schema = 'HHSurvey', tbl_name = 'v_trips_labels') %>%
  filter(survey_year %in% incl_years) %>%
  rename(hh_id = household_id)%>%
  filter(!is.na(arrival_time_second))%>% 
  select(-c("dest_x_coord","dest_y_coord","dest_tract20",
            "origin_x_coord","origin_y_coord","origin_tract20",
            "dwell_mins",
            "distance_meters","distance_miles","duration_minutes",
            "duration_seconds","speed_mph"))

write_csv(hh, file.path(HTS_data_dir,"v_households_labels.csv"))
write_csv(person, file.path(HTS_data_dir,"v_persons_labels.csv"))
write_csv(day, file.path(HTS_data_dir,"v_days_labels.csv"))
write_csv(trip, file.path(HTS_data_dir,"v_trips_labels.csv"))
