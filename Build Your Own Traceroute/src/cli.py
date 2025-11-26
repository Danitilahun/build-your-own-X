import argparse

def main():
    
    parser = argparse.ArgumentParser(description="""A simple tool to learn how to create Traceroute.
                                     Traceroute is a tool to that allows us to trace the route network packets 
                                     will take from one computer to another over a network.""")
    
    parser.add_argument('hostName',help="Write the name of the host.")
    
    args = parser.parse_args()
    
    print(args)
    
if __name__ == "__main__":
    main()