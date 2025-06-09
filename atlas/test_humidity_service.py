import time
from atlas_ide import AtlasIDEDiscovery

def test_humidity_service():
    print("Starting humidity service test...")
    
    # Create and start the IDE discovery service
    ide = AtlasIDEDiscovery()
    print("Starting Atlas IDE Discovery Service...")
    ide.start_discovery()
    
    try:
        # Wait for discovery (30 seconds timeout)
        timeout = 30
        start_time = time.time()
        thing_discovered = False
        
        print("Waiting for RaspberryHumidity to be discovered...")
        while time.time() - start_time < timeout:
            if "RaspberryHumidity" in ide.discovered_things:
                thing_discovered = True
                print("RaspberryHumidity discovered!")
                break
            time.sleep(1)
        
        if not thing_discovered:
            print("Error: RaspberryHumidity not discovered within timeout period")
            return False
        
        # Verify service exists
        if "Read_Humidity" not in ide.discovered_things["RaspberryHumidity"].services:
            print("Error: Read_Humidity service not found")
            return False
        
        print("\nService details:")
        service = ide.discovered_things["RaspberryHumidity"].services["Read_Humidity"]
        print(f"Name: {service.name}")
        print(f"Inputs: {service.inputs}")
        print(f"Outputs: {service.outputs}")
        print(f"Description: {service.description}")
        
        # Wait a bit to ensure service registration is processed
        print("\nWaiting for service registration to be processed...")
        time.sleep(5)
        
        # Try to invoke the service
        print("\nInvoking Read_Humidity service...")
        response = ide.invoke_service("RaspberryHumidity", "Read_Humidity")
        print(f"Service response: {response}")
        
        # Check if the response indicates success
        if "Service call successful" in response:
            print("\nTest passed! Service is working correctly.")
            return True
        else:
            print("\nTest failed! Service returned an error.")
            return False
            
    except Exception as e:
        print(f"Test failed with error: {str(e)}")
        return False
    finally:
        print("\nStopping Atlas IDE Discovery Service...")
        ide.stop_discovery()

if __name__ == "__main__":
    success = test_humidity_service()
    print(f"\nTest {'passed' if success else 'failed'}") 