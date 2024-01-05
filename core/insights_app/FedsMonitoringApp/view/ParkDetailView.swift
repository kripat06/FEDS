//
//  ParkDetailView.swift
//  FedsMonitoringApp
//
//  Created by Jagdish Patel on 3/10/23.
//

import SwiftUI

struct ParkDetailView: View {
    let park: Park
    
    @StateObject private var viewModel = BlocksFetcher()
    @StateObject private var statusViewModel = StatusFetcher()
    
    let timer = Timer.publish(every: 2, on: .current, in: .common).autoconnect()
    
    var xMultiple = 98
    var yMultiple = 78
    var fireDetectedInPark: Bool = false
    
    
    init(park: Park) {
        self.park = park
    }
    
    var body: some View {
        let size: CGFloat = 184
        let columns = [
            GridItem(.fixed(size), spacing: 0),
            GridItem(.fixed(size), spacing: 0),
            GridItem(.fixed(size), spacing: 0),
            GridItem(.fixed(size), spacing: 0),
        ]
        ScrollView {
            Spacer().frame(height: 0)
            VStack {
                HStack {
                    Spacer()
                    Text("\(park.name) National Park")
                        .font(.system(size: 45))
                        .bold()
                        .padding()
                    Spacer()
                }
                Spacer().frame(height: 150)
                AsyncImage(url: URL(string: park.park_map)) { image in
                    image
                        .resizable()
                        .aspectRatio(contentMode: .fill)
                        .overlay(
                            LazyVGrid(columns: columns, spacing: 0) {
                                ForEach(viewModel.blocks) { block in
                                    NavigationLink(destination: ParkStatusView(block: block, park: park)) {
                                        Rectangle()
                                            .fill(.clear)
                                            .border(Color.gray)
                                            .aspectRatio(1, contentMode: .fit)
                                            .overlay{
                                                if block.status == "Clear" {
                                                    Circle()
                                                        .fill(identifyColor(status: block.status))
                                                        .frame(width: 50)
                                                }
                                                else if block.status == "FireDetected" {
                                                    Circle()
                                                        .fill(identifyColor(status: block.status))
                                                        .frame(width: 50)
                                                    
                                                }
                                                else if block.status == "Extinguished" {
                                                    Circle()
                                                        .fill(identifyColor(status: block.status))
                                                        .frame(width: 50)
                                                    
                                                }
                                                else {
                                                    Circle()
                                                        .fill(identifyColor(status: block.status))
                                                        .frame(width: 50)
                                                }
                                            }
                                    }
                                }
                                
                            }
                                .padding(.horizontal)
                        )
                } placeholder: {
                    Image(systemName: "photo")
                        .resizable()
                        .scaledToFit()
                        .frame(width: 100, height: 100, alignment: .center)
                        .foregroundColor(.white.opacity(0.7))
                        .frame(maxWidth: .infinity, maxHeight: .infinity)
                }
                .frame(height: 300)
                .padding()
                
                Spacer()
                    .frame(height: 150)
                
                HStack {
                    Spacer()
                        .frame(width: 15)
                    RoundedRectangle(cornerRadius: 10)
                        .stroke(Color.gray, lineWidth: 1)
                        .frame(width: 170, height: 140)
                        .overlay {
                            VStack {
                                Spacer().frame(height: 20)
                                Text("Block Status")
                                    .font(.system(size: 20))
                                    .foregroundColor(.white)
                                    .bold()
                                Spacer().frame(height: 5)
                                Image(systemName: identifyBlockStatusIcon(blocks: self.viewModel.blocks))
                                    .font(.system(size: 40))
                                    .foregroundColor(identifyBlockStatusIconColor(blocks: self.viewModel.blocks))
                                Spacer().frame(height: 5)
                                Text(checkIfFireDetected(blocks: self.viewModel.blocks))
                                    .font(.system(size: 15))
                                    .foregroundColor(identifyBlockStatusColor(blocks: self.viewModel.blocks))
                                    .bold()
                                Spacer().frame(height: 20)
                            }
                        }
                    Spacer()
                    
                    RoundedRectangle(cornerRadius: 10)
                        .stroke(Color.gray, lineWidth: 1)
                        .frame(width: 170, height: 140)
                        .overlay {
                            VStack {
                                Spacer().frame(height: 20)
                                Text("Connectivity")
                                    .font(.system(size: 20))
                                    .foregroundColor(.white)
                                    .bold()
                                Spacer().frame(height: 5)
                                Image(systemName: identifyNetworkStatusIcon(networkStatus: self.statusViewModel.networkStatus))
                                    .font(.system(size: 42))
                                    .foregroundColor(.blue)
                                Spacer().frame(height: 5)
                                Text(identifyNetworkStatus(networkStatus: self.statusViewModel.networkStatus))
                                    .font(.system(size: 15))
                                    .foregroundColor(identifyNetworkStatusColor(networkStatus: self.statusViewModel.networkStatus))
                                    .bold()
                                Spacer().frame(height: 20)
                            }
                        }
                    Spacer()
                    
                    RoundedRectangle(cornerRadius: 10)
                        .stroke(Color.gray, lineWidth: 1)
                        .frame(width: 170, height: 140)
                        .overlay {
                            VStack {
                                Spacer().frame(height: 20)
                                Text("Scout Status")
                                    .font(.system(size: 20))
                                    .foregroundColor(.white)
                                    .bold()
                                Spacer().frame(height: 5)
                                Image(systemName: "eye.circle")
                                    .font(.system(size: 40))
                                    .foregroundColor(identifyScoutStatusColor(scoutStatus: self.statusViewModel.scoutStatus))
                                Spacer().frame(height: 5)
                                Text(identifyScoutStatus(scoutStatus: self.statusViewModel.scoutStatus))
                                    .font(.system(size: 15))
                                    .foregroundColor(identifyScoutStatusColor(scoutStatus: self.statusViewModel.scoutStatus))
                                    .bold()
                                Spacer().frame(height: 20)
                            }
                        }
                    Spacer()
                    
                    RoundedRectangle(cornerRadius: 10)
                        .stroke(Color.gray, lineWidth: 1)
                        .frame(width: 170, height: 140)
                        .overlay {
                            VStack {
                                Spacer().frame(height: 20)
                                Text("FEDS Status")
                                    .font(.system(size: 20))
                                    .foregroundColor(.white)
                                    .bold()
                                Spacer().frame(height: 5)
                                Image(systemName: identifyFedsStatusIcon(fedsStatus: self.statusViewModel.fedsStatus))
                                    .font(.system(size: 40))
                                    .foregroundColor(identifyFedsStatusColor(fedsStatus: self.statusViewModel.fedsStatus))
                                Spacer().frame(height: 5)
                                Text(identifyFedsStatus(fedsStatus: self.statusViewModel.fedsStatus))
                                    .font(.system(size: 15))
                                    .foregroundColor(identifyFedsStatusColor(fedsStatus: self.statusViewModel.fedsStatus))
                                    .bold()
                                Spacer().frame(height: 20)
                            }
                        }
                    Spacer()
                }
            }
        }
        .onAppear(perform: self.loadDetail)
                .refreshable(action: self.loadDetail)
                .onReceive(timer){ input in
                    self.loadDetail()
                }
    }
    
    func loadDetail() {
        self.viewModel.fetchBlocks(for: park.id)
        self.statusViewModel.fetchScoutStatus()
        self.statusViewModel.fetchNetworkStatus()
        self.statusViewModel.fetchFedsStatus()
    }
    
    func identifyColor(status:String) -> Color {
        if status == "Clear" {
            return Color.green
        }
        else if status == "FireDetected" {
            return Color.orange
        }
        else if status == "Extinguished" {
            return Color.blue
        }
        return Color.gray
    }
    
    func identifyScoutStatus(scoutStatus: ScoutStatus) -> String {
        if scoutStatus.navigate_flag {
            return "Active"
        }
        return "Inactive"
    }
    
    func identifyScoutStatusColor(scoutStatus: ScoutStatus) -> Color {
        if scoutStatus.navigate_flag {
            return Color.green
        }
        return Color.gray
    }
    
    func checkIfFireDetected(blocks: [Block]) -> String {
        var status = "Clear"
        blocks.forEach { block in
            if block.status == "FireDetected" {
                status = "Fire Detected"
            }
        }
        return status
    }
    
    func identifyBlockStatusColor(blocks: [Block]) -> Color {
        var c = Color.green
        blocks.forEach { block in
            if block.status == "FireDetected" {
                c = Color.red
            }
        }
        return c
    }
    
    func identifyBlockStatusIcon(blocks: [Block]) -> String {
        var c = "tree.circle"
        blocks.forEach { block in
            if block.status == "FireDetected" {
                c = "flame.circle"
            }
        }
        return c
    }
    
    func identifyBlockStatusIconColor(blocks: [Block]) -> Color {
        var c = Color.green
        blocks.forEach { block in
            if block.status == "FireDetected" {
                c = Color.orange
            }
        }
        return c
    }
    
    func identifyNetworkStatus(networkStatus: NetworkStatus) -> String {
        var s = "Good"
        if networkStatus.connectivity_flag == false {
            s = "Weak"
        }
        return s
    }
    
    func identifyNetworkStatusIcon(networkStatus: NetworkStatus) -> String {
        var i = "wifi"
        if networkStatus.connectivity_flag == false {
            i = "wifi.exclamationmark"
        }
        return i
    }
    
    func identifyNetworkStatusColor(networkStatus: NetworkStatus) -> Color {
        var c = Color.green
        if networkStatus.connectivity_flag == false {
            c = Color.red
        }
        return c
    }
    
    func identifyFedsStatus(fedsStatus: FedsStatus) -> String {
        var s = "Offline"
        if fedsStatus.offline_mode == false {
            s = "Online"
        }
        return s
    }
    

    func identifyFedsStatusIcon(fedsStatus: FedsStatus) -> String {
        var i = "xmark.seal"
        if fedsStatus.offline_mode == false {
            i = "checkmark.seal"
        }
        return i
    }
    
    func identifyFedsStatusColor(fedsStatus: FedsStatus) -> Color {
        var c = Color.gray
        if fedsStatus.offline_mode == false {
            c = Color.green
        }
        return c
    }
}

struct ParkDetailView_Previews: PreviewProvider {
    static var previews: some View {
        ParkDetailView(park: .init(id: 1,
                                   name: "Yosemite",
                                   park_map: "",
                                   park_image: "",
                                   county: "County1",
                                   fire_detected: false,
                                   system_up: true)
        )
    }
}
