package com.example.khite.wanderingwombats;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.TextView;

import java.lang.reflect.Array;
import java.util.Arrays;

public class TripDisplayActivity extends AppCompatActivity {

    int[] citiesArray;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_trip_display);

        // Get trip cities array from previous activity
        Bundle extras = getIntent().getExtras();
        citiesArray = extras.getIntArray("tripCities");

        // Display cities info
        TextView t = (TextView) findViewById(R.id.textView5);
        t.setText(Arrays.toString(citiesArray));
    }

    public void openDisplayMapActivity(View view){
        Intent intent = new Intent(this, DisplayMapActivity.class);
        intent.putExtra("bluetoothList", citiesArray);
        startActivity(intent);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_trip_display, menu);
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
