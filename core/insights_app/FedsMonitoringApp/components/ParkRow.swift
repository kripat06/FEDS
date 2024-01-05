//
//  ParkRow.swift
//  FedsMonitoringApp
//
//  Created by Krish Patel on 3/10/23.
//

import SwiftUI

struct ParkRow: View {
    let park: Park
    
    var body: some View {
        VStack {
            HStack {
                AsyncImage(url: URL(string: park.park_image)) { image in
                  image
                        .resizable()
                        .frame(width: 100, height: 80)
                        .aspectRatio(contentMode: .fill)
                } placeholder: {
                  Image(systemName: "photo")
                        .resizable()
                        .scaledToFit()
                        .frame(width: 40, height: 40, alignment: .center)
                        .foregroundColor(.white.opacity(0.7))
                        .frame(maxWidth: .infinity, maxHeight: .infinity)
                        .overlay(alignment: .bottom) {
                            Text(park.name)
                                .font(.headline)
                                .foregroundColor(.white)
                                .shadow(color: .black, radius: 3, x: 0, y: 0)
                                .frame(maxWidth: 136)
                                .padding()
                        }
                }
                .frame(width: 100, height: 80, alignment: .top)
                .background(LinearGradient(gradient: Gradient(colors: [Color(.gray).opacity(0.3), Color(.gray)]), startPoint: .top, endPoint: .bottom))
                .clipShape(RoundedRectangle(cornerRadius: 10, style: .continuous))
                .shadow(color: Color.black.opacity(0.3), radius: 15, x:0, y:10)
                .padding()
                
                Spacer()
                    .frame(width: 30)
                VStack(alignment: .leading) {
                    Text(park.name)
                        .fontWeight(.medium)
                        .font(.system(size: 30))
                    Text(park.county)
                }
                .frame(width: .infinity, height: 50, alignment: .top)

                Spacer()
                HStack {
                    if park.system_up {
                        Image(systemName: "antenna.radiowaves.left.and.right")
                            .font(.system(size: 40))
                            .foregroundColor(.green)

                    }
                    else {
                        Image(systemName: "antenna.radiowaves.left.and.right.slash")
                            .font(.system(size: 40))
                            .foregroundColor(.gray)
                    }
                    
                    
                    if park.fire_detected {
                        Image(systemName: "flame.fill")
                            .font(.system(size: 35))
                            .foregroundColor(.orange)
                    }
                    else {
                        if park.system_up {
                            Image(systemName: "tree.circle.fill")
                                .font(.system(size: 35))
                                .foregroundColor(Color(hue: 0.324, saturation: 0.987, brightness: 0.498))

                        }
                        else {
                            Image(systemName: "tree.circle.fill")
                                .font(.system(size: 35))
                                .foregroundColor(.gray)

                        }

                    }
                }
                .padding()
            }
            Divider()
        }
    }
}

//struct ParkRow_Previews: PreviewProvider {
//    static var previews: some View {
//        ParkRow()
//    }
//}
