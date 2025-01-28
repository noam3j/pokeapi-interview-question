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

class UrlContainer {
    public String url;
    
    public UrlContainer(String url) {
        this.url = url;
    }
}

class Species {
    
    public UrlContainer evolution_chain;
    public String name;
    
    public Species(UrlContainer evolution_chain, String name) {
        this.evolution_chain = evolution_chain;
        this.name = name;
    }
}

class EvolutionChain {
    
    public Chain chain;
    
    public EvolutionChain(Chain chain) {
        this.chain = chain;
    }
}

class Chain {
    
    public Species species;
    public List<EvolvesTo> evolves_to;
    
    public Chain(Species species, List<EvolvesTo> evolves_to) {
        this.species = species;
        this.evolves_to = evolves_to;
    }
}

class EvolvesTo {
    
    public Species species;
    public List<EvolvesTo> evolves_to;
    
    public EvolvesTo(Species species, List<EvolvesTo> evolves_to) {
        this.species = species;
        this.evolves_to = evolves_to;
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

public class MyClass {
    public static void main(String args[]) throws IOException {
        
        EvolutionChain evolutionChain = MyClass.getEvolutionChainForEevee();
        
        // Example printing as json
        Gson gson = new GsonBuilder().create();
        String jsonString = gson.toJson(evolutionChain);
        System.out.println(jsonString);
    }

    public static EvolutionChain getEvolutionChainForEevee() throws IOException {
        SimpleHttpClient client = new SimpleHttpClient();
        Species species = client.get("https://pokeapi.co/api/v2/pokemon-species/eevee", Species.class);
        EvolutionChain evolutionChain = client.get(species.evolution_chain.url, EvolutionChain.class);
        return evolutionChain;
    }
}