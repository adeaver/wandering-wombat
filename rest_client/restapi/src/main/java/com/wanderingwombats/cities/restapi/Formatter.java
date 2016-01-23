package com.wanderingwombats.cities.restapi;

import java.util.Map;

public class Formatter {
	
	public static String[] stringArrayFromObjectArray(Object[] input) {
		String[] output = new String[input.length];
		
		for(int index = 0; index < output.length; index++) {
			output[index] = input[index].toString();
		}
		
		return output;
	}
	
	public static CityInfo[] getCityInfoFromResp(Map<String, Object> response) {
		String[] cities = Formatter.getCityNamesFromResp(response);
		CityInfo[] cityInfoCollection = new CityInfo[cities.length];
		
		for(int index = 0; index < cityInfoCollection.length; index++) {
			Object[] cityObjects = (Object[]) response.get(cities[index]);
			String[] cityLocations = Formatter.stringArrayFromObjectArray(cityObjects);
			cityInfoCollection[index] = new CityInfo(cities[index], cityLocations);
		}
		
		return cityInfoCollection;
	}
	
	public static String[] getCityNamesFromResp(Map<String, Object> response) {
		return Formatter.stringArrayFromObjectArray((Object[]) response.get("cities"));

	}
}
