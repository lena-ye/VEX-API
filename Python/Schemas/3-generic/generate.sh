#!/bin/bash

# List of schemas from the website
schemas=(
  Event
  EventType
  Program
  EventLevel
  Location
  Coordinates
  Locations
  Division
  Grade
  Team
  IdInfo
  MatchObj
  Alliance
  AllianceTeam
  Ranking
  Skill
  SkillType
  Award
  TeamAwardWinner
  Season
  Error
  PageMeta
  PaginatedTeam
  PaginatedEvent
  PaginatedAward
  PaginatedSeason
  PaginatedRanking
  PaginatedMatch
  PaginatedSkill
  PaginatedProgram
)

original_file="00_schema_expanded.py" # MODIFY THIS PART - skeleton or expanded, depending on your needs
temp_file="schema_skeleton_temp.py"


for schema in "${schemas[@]}"; do
  echo "Running for schema: $schema"
  # Define schema_name to be items from the list above 
  sed "s/^schema_name = .*/schema_name = \"$schema\"/" "$original_file" > "$temp_file"
  
  # Result: .json document generation
  python "$temp_file" 
done

rm "$temp_file"
