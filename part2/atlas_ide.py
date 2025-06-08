import socket
import json
import threading
import time
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional
from dataclasses import dataclass
from queue import Queue

@dataclass
class AtlasService:
    name: str
    inputs: str
    outputs: str
    description: Optional[str] = None
    libraries: List[str] = None
    functionality: Optional[str] = None

@dataclass
class AtlasEntity:
    entity_id: str
    entity_name: str
    entity_type: str
    sensor_actuator: str
    description: str
    services: Dict[str, AtlasService]

@dataclass
class AtlasThing:
    thing_id: str
    space_id: str
    thing_name: str
    thing_type: str
    description: str
    entities: Dict[str, AtlasEntity]
    services: Dict[str, AtlasService]
    relationships: List[dict]

class AtlasIDEDiscovery:
    def __init__(self, host: str = '127.0.0.1', port: int = 6668, multicast_group: str = '232.1.1.1', multicast_port: int = 1235):
        self.host = host
        self.port = port
        self.multicast_group = multicast_group
        self.multicast_port = multicast_port
        self.discovered_things: Dict[str, AtlasThing] = {}
        self.tweet_queue = Queue()
        self.running = False
        self.discovery_thread = None
        self.command_socket = None

    def start_discovery(self):
        """Start the background discovery service"""
        if self.running:
            return
        
        self.running = True
        self.discovery_thread = threading.Thread(target=self._discovery_loop)
        self.discovery_thread.daemon = True
        self.discovery_thread.start()

    def stop_discovery(self):
        """Stop the background discovery service"""
        self.running = False
        if self.discovery_thread:
            self.discovery_thread.join()
        if self.command_socket:
            self.command_socket.close()

    def _discovery_loop(self):
        """Main discovery loop that listens for multicast tweets"""
        while self.running:
            try:
                # Create UDP socket for multicast
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                
                # Bind to the multicast port
                sock.bind(('', self.multicast_port))
                
                # Join the multicast group
                mreq = socket.inet_aton(self.multicast_group) + socket.inet_aton('0.0.0.0')
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
                
                print(f"Listening for multicast tweets on {self.multicast_group}:{self.multicast_port}")
                
                while self.running:
                    try:
                        data, addr = sock.recvfrom(4096)
                        if data:
                            try:
                                tweet = json.loads(data.decode('utf-8'))
                                self._process_tweet(tweet)
                            except json.JSONDecodeError:
                                print(f"Error decoding tweet: {data.decode('utf-8')}")
                            except Exception as e:
                                print(f"Error processing tweet: {e}")
                    except Exception as e:
                        print(f"Socket error: {e}")
                        break
            except Exception as e:
                print(f"Discovery error: {e}")
                time.sleep(5)

    def _process_tweet(self, tweet: dict):
        """Process different types of tweets to discover things and services"""
        tweet_type = tweet.get("Tweet Type")
        print(f"\nReceived tweet type: {tweet_type}")
        print(f"Tweet content: {json.dumps(tweet, indent=2)}")
        
        if tweet_type == "Identity_Thing":
            self._handle_thing_identity(tweet)
        elif tweet_type == "Service":
            self._handle_service_tweet(tweet)
        elif tweet_type == "Relationship":
            self._handle_relationship_tweet(tweet)
        elif tweet_type == "Entity Identity":
            self._handle_entity_identity(tweet)
        elif tweet_type == "Identity_Language":
            self._handle_identity_language(tweet)
            
        # Add default service for RaspberryHumidity if we see its identity
        if tweet_type in ["Identity_Thing", "Identity_Language"]:
            thing_id = tweet.get("Thing ID")
            if thing_id == "RaspberryHumidity" and thing_id not in self.discovered_things:
                self.discovered_things[thing_id] = AtlasThing(
                    thing_id=thing_id,
                    space_id=tweet.get("Space ID", "MySmartSpace"),
                    thing_name=tweet.get("Name", thing_id),
                    thing_type=tweet.get("Model", "Unknown"),
                    description=tweet.get("Description", ""),
                    entities={},
                    services={},
                    relationships=[]
                )
                # Add default service
                service = AtlasService(
                    name="getHumidity",
                    inputs="()",
                    outputs="int",
                    description="Reads humidity from MCP3008 channel 0"
                )
                self.discovered_things[thing_id].services["getHumidity"] = service
                print(f"Added default service getHumidity for {thing_id}")

    def _handle_identity_language(self, tweet: dict):
        """Handle identity language tweets"""
        thing_id = tweet.get("Thing ID")
        space_id = tweet.get("Space ID")
        
        if thing_id and space_id:
            print(f"Thing {thing_id} in space {space_id} announced its language")
            # Create thing if it doesn't exist
            if thing_id not in self.discovered_things:
                self.discovered_things[thing_id] = AtlasThing(
                    thing_id=thing_id,
                    space_id=space_id,
                    thing_name=thing_id,  # Use ID as name if not provided
                    thing_type="Unknown",
                    description="",
                    entities={},
                    services={},
                    relationships=[]
                )
                print(f"Created new thing entry for {thing_id}")

    def _handle_thing_identity(self, tweet: dict):
        """Handle thing identity tweets"""
        thing_id = tweet.get("Thing ID")
        space_id = tweet.get("Space ID")
        
        if thing_id and space_id:
            if thing_id not in self.discovered_things:
                self.discovered_things[thing_id] = AtlasThing(
                    thing_id=thing_id,
                    space_id=space_id,
                    thing_name=tweet.get("Name", thing_id),
                    thing_type=tweet.get("Model", "Unknown"),
                    description=tweet.get("Description", ""),
                    entities={},
                    services={},
                    relationships=[]
                )
                print(f"Discovered new thing: {thing_id} ({tweet.get('Name', thing_id)}) in space {space_id}")
                
                # Add default service from IoTDDL
                if thing_id == "RaspberryHumidity":
                    service = AtlasService(
                        name="getHumidity",
                        inputs="()",
                        outputs="int",
                        description="Reads humidity from MCP3008 channel 0"
                    )
                    self.discovered_things[thing_id].services["getHumidity"] = service
                    print(f"Added default service getHumidity for {thing_id}")

    def _handle_service_tweet(self, tweet: dict):
        """Handle service tweets"""
        thing_id = tweet.get("Thing ID")
        service_name = tweet.get("Service Name")
        
        if thing_id and service_name:
            # Create thing if it doesn't exist
            if thing_id not in self.discovered_things:
                self._handle_identity_language({
                    "Tweet Type": "Identity_Language",
                    "Thing ID": thing_id,
                    "Space ID": tweet.get("Space ID", "MySmartSpace")
                })
            
            service = AtlasService(
                name=service_name,
                inputs=tweet.get("Service Inputs", ""),
                outputs=tweet.get("Service Outputs", ""),
                description=tweet.get("Service Description"),
                libraries=tweet.get("Libraries", []),
                functionality=tweet.get("Functionality")
            )
            self.discovered_things[thing_id].services[service_name] = service
            print(f"Discovered service {service_name} for thing {thing_id}")

    def _handle_entity_identity(self, tweet: dict):
        """Handle entity identity tweets"""
        thing_id = tweet.get("Thing ID")
        entity_id = tweet.get("Entity ID")
        
        if thing_id and entity_id:
            # Create thing if it doesn't exist
            if thing_id not in self.discovered_things:
                self._handle_identity_language({
                    "Tweet Type": "Identity_Language",
                    "Thing ID": thing_id,
                    "Space ID": tweet.get("Space ID", "MySmartSpace")
                })
            
            entity = AtlasEntity(
                entity_id=entity_id,
                entity_name=tweet.get("Entity Name", entity_id),
                entity_type=tweet.get("Entity Type", "Unknown"),
                sensor_actuator=tweet.get("Entity SensorActuator", "Unknown"),
                description=tweet.get("Entity Description", ""),
                services={}
            )
            self.discovered_things[thing_id].entities[entity_id] = entity
            print(f"Discovered entity {entity_id} ({entity.entity_name}) for thing {thing_id}")

    def _handle_relationship_tweet(self, tweet: dict):
        """Handle relationship tweets"""
        thing_id = tweet.get("Thing ID")
        
        if thing_id:
            # Create thing if it doesn't exist
            if thing_id not in self.discovered_things:
                self._handle_identity_language({
                    "Tweet Type": "Identity_Language",
                    "Thing ID": thing_id,
                    "Space ID": tweet.get("Space ID", "MySmartSpace")
                })
            
            self.discovered_things[thing_id].relationships.append(tweet)
            print(f"Discovered relationship for thing {thing_id}")

    def invoke_service(self, thing_id: str, service_name: str, inputs: str = "()") -> str:
        """Invoke a service on a thing"""
        if thing_id not in self.discovered_things:
            return f"Error: Thing {thing_id} not found"
        
        if service_name not in self.discovered_things[thing_id].services:
            return f"Error: Service {service_name} not found for thing {thing_id}"
        
        try:
            # Format the service call according to Atlas middleware requirements
            service_call = {
                "Tweet Type": "API Call",
                "Thing ID": thing_id,
                "Space ID": self.discovered_things[thing_id].space_id,
                "Service Name": service_name,
                "Service Inputs": inputs
            }
            
            print(f"\nInvoking service {service_name} on thing {thing_id}")
            print(f"Service call: {json.dumps(service_call, indent=2)}")
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # Set socket options
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                
                # Connect and send service call
                sock.connect((self.host, self.port))
                sock.sendall((json.dumps(service_call) + "\n").encode('utf-8'))
                
                # Wait for response
                response = sock.recv(4096).decode('utf-8').strip()
                
                try:
                    # Try to parse response as JSON
                    response_json = json.loads(response)
                    if "Status" in response_json:
                        status = response_json["Status"]
                        if status == "Successful":
                            return f"Service call successful: {response_json.get('Service Outputs', 'No output')}"
                        else:
                            return f"Service call failed: {response_json.get('Status Description', 'Unknown error')}"
                    return response
                except json.JSONDecodeError:
                    # If response is not JSON, return as is
                    return response
                
        except ConnectionRefusedError:
            return "Error: Could not connect to Atlas middleware"
        except Exception as e:
            return f"Error invoking service: {str(e)}"

    def print_discovery_status(self):
        """Print the current discovery status"""
        print("\n=== Atlas IDE Discovery Status ===")
        if not self.discovered_things:
            print("No things discovered yet")
            return
            
        for thing_id, thing in self.discovered_things.items():
            print(f"\nThing: {thing.thing_name} ({thing_id})")
            print(f"Space: {thing.space_id}")
            print(f"Type: {thing.thing_type}")
            print(f"Description: {thing.description}")
            
            if thing.entities:
                print("\nEntities:")
                for entity_id, entity in thing.entities.items():
                    print(f"  - {entity.entity_name} ({entity_id})")
                    print(f"    Type: {entity.entity_type}")
                    print(f"    Role: {entity.sensor_actuator}")
                    print(f"    Description: {entity.description}")
            
            if thing.services:
                print("\nServices:")
                for service_name, service in thing.services.items():
                    print(f"  - {service_name}")
                    print(f"    Inputs: {service.inputs}")
                    print(f"    Outputs: {service.outputs}")
                    if service.description:
                        print(f"    Description: {service.description}")
            
            if thing.relationships:
                print("\nRelationships:")
                for rel in thing.relationships:
                    print(f"  - {rel.get('Relationship Type', 'Unknown')}")

def main():
    # Create and start the IDE discovery service
    ide = AtlasIDEDiscovery()
    print("Starting Atlas IDE Discovery Service...")
    ide.start_discovery()
    
    try:
        while True:
            print("\nAtlas IDE Commands:")
            print("1. status - Show discovery status")
            print("2. invoke <thing_id> <service_name> [inputs] - Invoke a service")
            print("3. help - Show this help message")
            print("4. exit - Exit the IDE")
            
            command = input("\natlas> ").strip()
            
            if command == "exit":
                break
            elif command == "status":
                ide.print_discovery_status()
            elif command == "help":
                print("\nAvailable commands:")
                print("  status - Show discovery status")
                print("  invoke <thing_id> <service_name> [inputs] - Invoke a service")
                print("  help - Show this help message")
                print("  exit - Exit the IDE")
                print("\nExample service calls:")
                print("  invoke RaspberryHumidity getHumidity")
            elif command.startswith("invoke "):
                parts = command.split()
                if len(parts) >= 3:
                    thing_id = parts[1]
                    service_name = parts[2]
                    inputs = parts[3] if len(parts) > 3 else "()"
                    response = ide.invoke_service(thing_id, service_name, inputs)
                    print(f"\nService response: {response}")
                else:
                    print("Usage: invoke <thing_id> <service_name> [inputs]")
                    print("Example: invoke RaspberryHumidity getHumidity")
            else:
                print("Unknown command. Type 'help' for available commands.")
    except KeyboardInterrupt:
        print("\nStopping Atlas IDE Discovery Service...")
    finally:
        ide.stop_discovery()

if __name__ == "__main__":
    main() 