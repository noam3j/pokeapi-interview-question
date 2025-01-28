import org.apache.http.HttpEntity;
import org.apache.http.HttpHeaders;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import java.io.IOException;
import java.util.List;
import java.util.Arrays;

class Move {
    String name;
    String url;
    
    public Move(String name, String url) {
        this.name = name;
        this.url = url;
    }
}

class PokemonType {
    String name;
    List<Move> moves;
    
    public PokemonType(String name, List<Move> moves) {
        this.name = name;
        this.moves = moves;
    }
}

class SimpleHttpClient {
    public <T> T get(String url, Class<T> clazz) throws IOException {
        CloseableHttpClient httpClient = HttpClients.createDefault();
        
        try {
            HttpGet request = new HttpGet(url);        
            CloseableHttpResponse response = httpClient.execute(request);
            
            try {
                HttpEntity entity = response.getEntity();
                String responseString = EntityUtils.toString(entity);
                    
                Gson gson = new GsonBuilder().create();
                return gson.fromJson(responseString, clazz);
                
            } finally {
                response.close();
            }
        } finally {
            httpClient.close();
        }
    }
}

class Solution {
  public static void main(String args[]) throws IOException {
    SimpleHttpClient client = new SimpleHttpClient();
    PokemonType type = client.get("https://pokeapi.co/api/v2/type/water", PokemonType.class);
    
    // Example accessing/printing values
    System.out.println("name: " + type.name); //water
    System.out.println("first move (name): " + type.moves.get(0).name); //water-gun
    System.out.println("first move (url): " + type.moves.get(0).url); //https://pokeapi.co/api/v2/move/55/
    
    // Example printing as json
    Gson gson = new GsonBuilder().create();
    String jsonString = gson.toJson(type);
    System.out.println("type as json: " + jsonString);
  }
}