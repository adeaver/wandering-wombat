package com.wanderingwombats.cities.restapi;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.HashMap;
import java.util.Map;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class RequestClient {
	public final String API_URL = "/api/getLocations";
	
	public Map<String, Object> makeRequest(String requestParams) {
		return makeRequest(requestParams, 0);
	}
	
	public Map<String, Object> makeRequest(String requestParams, int cityCount) {
		HashMap<String, Object> returnValue = new HashMap<String, Object>();
		
		try {
			String url = DefaultValues.BASE_URL + API_URL + "?q=" + URLEncoder.encode(requestParams, "utf-8");
			url += cityCount != 0 ? "&count=" + URLEncoder.encode(String.valueOf(cityCount), "utf-8") : "";
			
			URL sendUrl = new URL(url);
			HttpURLConnection urlConnection = (HttpURLConnection) sendUrl.openConnection();
			
			BufferedReader br = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
			
			String line = "", finalResponse = "";
			
			while((line = br.readLine()) != null) {
				finalResponse += line;
			}
			
			JSONObject container = new JSONObject(finalResponse);
			JSONObject data = container.getJSONObject("data");
			
			JSONArray cityNames = data.getJSONArray("cities");
			String[] cityNamesStrings = jsonArrayToStringArray(cityNames);
			
			returnValue.put("response", container.get("response"));
			returnValue.put("cities", cityNamesStrings);
			
			for(String cityName : cityNamesStrings) {
				JSONArray cityInfo = data.getJSONArray(cityName);
				returnValue.put(cityName, jsonArrayToStringArray(cityInfo));
			}
			
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			returnValue.put("response", "You got Trumped");
			returnValue.put("data", new String[0]);
		}
		
		return returnValue;
	}
	
	private String[] jsonArrayToStringArray(JSONArray array) {
		String[] stringArray = new String[array.length()];
		
		for(int index = 0; index < array.length(); index++) {
			try {
				stringArray[index] = array.get(index).toString();
			} catch (JSONException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		
		return stringArray;
	}
}
