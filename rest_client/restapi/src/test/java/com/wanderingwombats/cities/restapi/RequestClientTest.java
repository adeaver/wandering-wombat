package com.wanderingwombats.cities.restapi;

import java.util.HashMap;

import junit.framework.TestCase;

import org.json.JSONException;
import org.junit.Test;

public class RequestClientTest extends TestCase {
	public RequestClient requestClient;
	
	@Override
	public void setUp() {
		requestClient = new RequestClient();
	}
	
	@Test
	public void testConnection() throws JSONException {
		HashMap<String, Object> returnValue = (HashMap<String, Object>) requestClient.makeRequest(DefaultValues.MUSEUMS);
		
		assertEquals("America is great", returnValue.get("response").toString());
	}
	
	@Test
	public void testAllConnections() throws JSONException {
		String[] channels = {DefaultValues.LANDMARKS, DefaultValues.ARCHITECTURE,
				DefaultValues.RELIGION, DefaultValues.HISTORY, DefaultValues.SPORTS,
				DefaultValues.MUSEUMS, DefaultValues.ART, DefaultValues.SCIENCE,
				DefaultValues.NATURE, DefaultValues.THEATER, DefaultValues.SHOPPING};
		
		for(String channel : channels) {
			System.err.println(channel);
			HashMap<String, Object> returnValue = (HashMap<String, Object>) requestClient.makeRequest(channel);
			
			try {
				assertEquals("America is great", returnValue.get("response").toString());
			} catch(Exception e) {
				e.printStackTrace();
			}
		}
	}
}
