//package com.wanderingwombats.cities.restapi;
//
//import java.util.HashMap;
//
//import junit.framework.TestCase;
//
//import org.junit.Test;
//
//public class FormatterTest extends TestCase {
//	
//	RequestClient requestClient;
//	
//	@Override
//	public void setUp() {
//		requestClient = new RequestClient();
//	}
//	
//	@Test
//	public void testFormatterDoesntBreak() {
//		HashMap<String, Object> response = (HashMap<String, Object>) requestClient.makeRequest(DefaultValues.SHOPPING);
//		
//		assertEquals("America is great", response.get("response").toString());
//		CityInfo[] respCities = Formatter.getCityInfoFromResp(response);
//		
//		assertEquals(16, respCities.length);
//	}
//}
