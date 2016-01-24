package com.example.khite.wanderingwombats;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Toast;

public class NewTripActivity extends AppCompatActivity {

    EditText nameEdit;
    String tripName;
    String tripType;
    String numCities;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_new_trip);

        // Populate Dropdown List of Trip Types
        Spinner dropdown = (Spinner)findViewById(R.id.spinner1);
        dropdown.setPrompt("Choose a Trip Type");
        String[] items = new String[]{"Art", "Religion", "Architecture", "Landmarks", "History", "Sports", "Museums", "Science", "Nature", "Theater", "Shopping"};
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(this, android.R.layout.simple_spinner_dropdown_item, items);
        dropdown.setAdapter(adapter);

        Spinner dropdownNum = (Spinner)findViewById(R.id.spinner);
        dropdownNum.setPrompt("Choose a Trip Type");
        String[] itemsNum = new String[]{"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16"};
        ArrayAdapter<String> adapterNum = new ArrayAdapter<String>(this, android.R.layout.simple_spinner_dropdown_item, itemsNum);
        dropdownNum.setAdapter(adapterNum);
    }

    public void openTripDisplayActivity(View view){
        // Get Trip Name
        nameEdit = (EditText)findViewById(R.id.editText);
        tripName = nameEdit.getText().toString();

        // Get trip type
        Spinner dropdown = (Spinner) findViewById(R.id.spinner1);
        tripType = dropdown.getSelectedItem().toString();

        // Get number of cities
        Spinner dropdownNum = (Spinner) findViewById(R.id.spinner);
        numCities = dropdownNum.getSelectedItem().toString();

        // Calculating trip message
        Toast.makeText(NewTripActivity.this, "Calculating Trip ...",
                Toast.LENGTH_LONG).show();

        // Request trip from server, pass into array of location values for arduino and
        int[] tripArray = {7, 2, 5, 12, 14};

        // Open trip display activity and pass through trip information
        Intent intent = new Intent(this, TripDisplayActivity.class);
        intent.putExtra("tripCities", tripArray);
        startActivity(intent);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_new_trip, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}
