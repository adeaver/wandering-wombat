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
		HashMap<String, Object> returnValue = (HashMap<String, Object>) requestClient.makeRequest(DefaultValues.SPORTS);
		
		assertEquals("America is great", returnValue.get("response").toString());
	}
}
