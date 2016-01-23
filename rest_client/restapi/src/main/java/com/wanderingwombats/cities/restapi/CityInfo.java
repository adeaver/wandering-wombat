package com.wanderingwombats.cities.restapi;

public class CityInfo {
	String cityName;
	String[] cityLocations;
	
	public CityInfo(String name, String[] points) {
		cityName = name;
		cityLocations = points;
	}
	
	public String getCityName() {
		return cityName;
	}
	
	public String[] getCityLocations() {
		return cityLocations;
	}
}
