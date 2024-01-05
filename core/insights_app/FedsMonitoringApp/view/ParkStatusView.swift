//
//  ParkStatusView.swift
//  FedsMonitoringApp
//
//  Created by Krish Patel on 3/11/23.
//

import SwiftUI

struct ParkStatusView: View {
    let block: Block
    let park: Park
    
    init(block: Block, park: Park) {
        self.block = block
        self.park = park
    }
    
    var body: some View {
        Spacer().frame(height: 0)
        ScrollView {
            VStack {
                HStack {
                    Spacer()
                    Text("\(park.name) National Park")
                        .font(.system(size: 45))
                        .bold()
                        .padding()
                    Spacer()
                }

                Spacer()
                    .frame(height: 150)

                AsyncImage(url: URL(string: block.url)) { image in
                  image
                        .resizable()
                        .aspectRatio(contentMode: .fill)
                } placeholder: {
                  Image(systemName: "photo")
                        .resizable()
                        .scaledToFit()
                        .frame(width: 100, height: 100, alignment: .center)
                        .foregroundColor(.white.opacity(0.7))
                        .frame(maxWidth: .infinity, maxHeight: .infinity)
                }
                .frame(width: nil, height: 300)
                .padding()
                
                Spacer().frame(height: 180)
                
                HStack {
                    Spacer()
                    Text("Latitude: \(block.latitude), Longitude: \(block.longitude)")
                        .font(.system(size: 20))
                        .bold()
                        .padding()
                    Spacer()
                    Text("Fire Detected: \(identifyStatus(status: block.is_detected))")
                        .font(.system(size: 20))
                        .bold()
                        .padding()
                    Spacer()
                }
                HStack {
                    Spacer()
                    Text("\(Date(milliseconds:block.time_in_millis))")
                        .font(.system(size: 20))
                        .bold()
                        .padding()
                    Spacer()
                }
            }
            
        }
    }

    func identifyStatus(status:Bool) -> String {
        if status == true {
            return "Yes"
        }
        return "No"
    }

}


struct ParkStatusView_Previews: PreviewProvider {
    static var previews: some View {
        ParkStatusView(block: .init(
                                id: 1,
                                latitude: 1,
                                longitude: 1,
                                time_in_millis: 1679120100397,
                                url: "https://kpat-esp32fedsupload-west-2.s3.us-west-2.amazonaws.com/02_18_2023_06_17_23_esp32-1.jpg",
                                is_detected: true,
                                status: "FireDetected"
                              ),
                       park: .init(id: 1,
                                  name: "Yosemite",
                                  park_map: "",
                                  park_image: "",
                                  county: "County1",
                                  fire_detected: false,
                                  system_up: true)
        )
    }
}
