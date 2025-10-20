# El código generado con IA va desde las lineas que empienzan con el comentario "# /IA" hasta el siguiente comentario "# IA"
import tkinter as tk
from tkinter import ttk
import logic as l
from logic import add_client, general_queue, priority_queue, queue_to_list, copy_queue, copy_priority_queue, add_action, undo, products
import constants as c
from tkinter import PhotoImage

class MainUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Turnos")
        self.root.geometry("1280x720")
        self.root.config(bg="#faf9f7")
        self.root.iconbitmap("./res/burger.ico")

        self.type_selected = None
        self.counter = 1
        self.products_added = []


        # Estilos
        # IA
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 11), padding=10)
        self.style.configure("Title.TLabel", font=("Arial", 28, "bold"), foreground="#2d2d2d", background="#faf9f7")
        self.style.configure("Subtitle.TLabel", font=("Arial", 11), foreground="#888", background="#faf9f7")
        self.style.configure("Card.TFrame", background="white", relief="flat", borderwidth=1)
        self.style.configure("CardLabel.TLabel", background="white", font=("Arial", 11))
        self.style.configure("SectionTitle.TLabel", background="white", font=("Arial", 12, "bold"))
        self.style.configure("Counter.TLabel", background="#f8f2ec", foreground="#7a4c2d", font=("Arial", 10, "bold"))
        # /IA

        self.style.configure("TEntry", font=("Arial", 16), padding=10)
        self.style.configure("Selected.TButton", foreground="#f8862e")

        # Titulo
        self.frame_title = tk.Frame(self.root, bg="#faf9f7")
        self.frame_title.pack(pady=30)

        ttk.Label(self.frame_title, text="Sistema de Turnos", style="Title.TLabel").pack()
        
        ttk.Label(self.frame_title, text="Gestión de cola del restaurante", style="Subtitle.TLabel").pack()

        # Frame principal
        self.frame_main = tk.Frame(self.root, bg="#faf9f7")
        self.frame_main.pack(expand=True, fill="both", padx=40, pady=20)

        self.frame_main.columnconfigure(0, weight=1)
        self.frame_main.columnconfigure(1, weight=2)

        # Frame del formulario y acciones
        self.frame_left = ttk.Frame(self.frame_main, style="Card.TFrame", padding=20)
        self.frame_left.grid(row=0, column=0, sticky="nsew", padx=(0, 20), pady=10)

        self.label_name = ttk.Label(self.frame_left, text="Nombre del Cliente", style="SectionTitle.TLabel")
        self.label_name.pack(anchor="w")


        self.entry_name = ttk.Entry(self.frame_left, style="TEntry")
        self.entry_name.pack(fill="x", pady=5)

        ttk.Label(self.frame_left, text="Tipo de Cliente", style="SectionTitle.TLabel").pack(anchor="w", pady=(10, 5))

        self.frame_types = tk.Frame(self.frame_left, bg="white")
        self.frame_types.pack(pady=5, fill="x")

        self.btn_regular = ttk.Button(self.frame_types, text="👥 Regular")
        self.btn_regular.bind("<Button-1>", self.on_client_type_change)
        self.btn_regular.pack(side="left", expand=True, fill="x", padx=5)

        self.btn_vip = ttk.Button(self.frame_types, text="👑 Prioritario")
        self.btn_vip.bind("<Button-1>", self.on_client_type_change)
        self.btn_vip.pack(side="left", expand=True, fill="x", padx=5)

        self.btn_online = ttk.Button(self.frame_types, text="🌐 Domicilio/Online")
        self.btn_online.bind("<Button-1>", self.on_client_type_change)
        self.btn_online.pack(side="left", expand=True, fill="x", padx=5)

        self.frame_options = tk.Frame(self.frame_left, bg="white")
        self.frame_options.pack(pady=5, fill="x")

        self.btn_menu = ttk.Button(self.frame_options, text="🍔 Menu", style="TButton")
        self.btn_menu.bind("<Button-1>", self.on_menu)
        self.btn_menu.pack(side="left", expand=True, fill="x", padx=5)

        self.btn_add_to_queue = ttk.Button(self.frame_options, text="➕ Agregar a la Cola", style="TButton")
        self.btn_add_to_queue.bind("<Button-1>", self.on_add_to_queue)
        self.btn_add_to_queue.pack(side="left", expand=True, fill="x", padx=5)

        # Acciones
        self.frame_actions = tk.Frame(self.frame_left, bg="white")
        self.frame_actions.pack(fill="x", pady=10)

        self.btn_next = tk.Button(self.frame_actions, text="→ Llamar Siguiente", bg="#f7b98a", fg="black", font=("Arial", 11, "bold"), bd=0, relief="ridge")
        self.btn_next.bind("<Button-1>", self.on_call_next)
        self.btn_next.pack(fill="x", expand=True, side=tk.LEFT)

        self.btn_complete = tk.Button(self.frame_actions, text="✓Completar Servicio", bg="#f2f0ed", fg="gray30", font=("Arial", 11, "bold"), bd=0, relief="ridge")
        self.btn_complete.bind("<Button-1>", self.on_complete_service)
        self.btn_complete.pack(fill="x", expand=True, side=tk.LEFT, padx=(10, 0))

        # Turno actual
        self.frame_turn = ttk.Frame(self.frame_left, style="Card.TFrame", padding=20)
        self.frame_turn.pack(fill="x", pady=(10, 0))

        ttk.Label(self.frame_turn, text="Turno Actual", style="SectionTitle.TLabel").pack(pady=(0, 5))
        ttk.Label(self.frame_turn, text="--", font=("Arial", 20, "bold"), background="white", foreground="#999").pack()
        ttk.Label(self.frame_turn, text="No hay turno activo", background="white", foreground="#999").pack(pady=5)

        # Panel de la cola
        self.frame_right = ttk.Frame(self.frame_main, style="Card.TFrame", padding=20)
        self.frame_right.grid(row=0, column=1, sticky="nsew", pady=10)

        self.frame_header = tk.Frame(self.frame_right, bg="white")
        self.frame_header.pack(fill="x")

        self.btn_undo = tk.Button(self.frame_header, text="↩Deshacer", bg="#f7e4d3", fg="#333", font=("Arial", 10, "bold"), relief="flat", cursor="hand2")
        self.btn_undo.bind("<Button-1>", self.on_undo)
        self.btn_undo.pack(side="right", padx=(10, 0))

        ttk.Label(self.frame_header, text="🕒 Cola de Espera", style="SectionTitle.TLabel").pack(side="left")
        self.ticket_label = ttk.Label(self.frame_header, text="0 Turnos", style="Counter.TLabel")
        self.ticket_label.pack(side="right", padx=5)

        # Lista con scrollbar
        # IA
        self.canvas = tk.Canvas(self.frame_right, bg="white", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar = ttk.Scrollbar(self.frame_right, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        # /IA

        self.frame_queue = tk.Frame(self.canvas, bg="white")

        # IA
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas_window = self.canvas.create_window((0,0), window=self.frame_queue, anchor="nw")
        # /IA

        # Mensaje de cola vacía
        self.icon_queue = tk.Label(self.frame_queue, text="👥", font=("Arial", 40), bg="white", fg="#ccc")
        self.icon_queue.pack(pady=10)
        self.msg_queue = tk.Label(self.frame_queue, text="No hay clientes en espera", font=("Arial", 11), fg="#999", bg="white")
        self.msg_queue.pack()


        self.frame_queue.bind("<Configure>", self.on_configure)
        
        # IA
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        # /IA


    # Acciones de la interfaz
    # IA
    def on_configure(self, event=None):
        # Actualiza la región de desplazamiento del canvas para que abarque todo el contenido visible dentro (ajusta el scroll)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mousewheel(self, event):
            self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def on_canvas_configure(self, event):
        # Ajusta el ancho del frame interno al del canvas visible
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)
    # /IA

    def refresh_queue(self):
        # IA
        # Limpia la UI anterior
        for widget in self.frame_queue.winfo_children():
            widget.destroy()
        # /IA

        priority_queue_list = queue_to_list(copy_priority_queue(priority_queue))
        general_queue_list = queue_to_list(copy_queue(general_queue))
        total = len(priority_queue_list) + len(general_queue_list)
        self.ticket_label.config(text=f"{total} turnos")

        if total==0:
            self.icon_queue = tk.Label(self.frame_queue, text="👥", font=("Arial", 40), bg="white", fg="#ccc")
            self.icon_queue.pack(pady=10)
            self.msg_queue = tk.Label(self.frame_queue, text="No hay clientes en espera", font=("Arial", 11), fg="#999", bg="white")
            self.msg_queue.pack()
        else:
            for (priority, n, client) in priority_queue_list:
                card = TicketCard(self.frame_queue, client.n_order, client.name, client.id, client.type, len(client.order))
                card.pack(fill="x", pady=5)

            for client in general_queue_list:
                card = TicketCard(self.frame_queue, client.n_order, client.name, client.id, client.type, len(client.order))
                card.pack(fill="x", pady=5)

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    # Mostrar el seleccionado
    def on_client_type_change(self, event=None):
        if (event.widget.winfo_id() == self.btn_regular.winfo_id()):
            # IA
            self.btn_regular.config(style="Selected.TButton")
            self.btn_vip.config(style="TButton")
            self.btn_online.config(style="TButton")
            # /IA

            self.type_selected = "REGULAR"
        elif (event.widget.winfo_id() == self.btn_vip.winfo_id()):
            self.btn_vip.config(style="Selected.TButton")
            self.btn_regular.config(style="TButton")
            self.btn_online.config(style="TButton")

            self.type_selected = "VIP"
        else:
            self.btn_online.config(style="Selected.TButton")
            self.btn_regular.config(style="TButton")
            self.btn_vip.config(style="TButton")

            self.type_selected = "ONLINE"
        
    def on_add_to_queue(self, event=None):
        if (len(self.entry_name.get()) > 0 and self.type_selected != None and len(self.products_added) > 0):
            # Agregar lo datos del cleinte en la cola que corresponde
            add_client(self.entry_name.get(), self.type_selected, self.counter, self.products_added)
            
            # Restablecer a lo valores por defecto
            self.btn_regular.config(style="TButton")
            self.btn_vip.config(style="TButton")
            self.btn_online.config(style="TButton")
            self.entry_name.delete(0, len(self.entry_name.get()))
            self.counter = self.counter + 1
            self.products_added = []
            self.refresh_queue()

    def on_call_next(self, event=None):
        # Logica para llamar al siguinte cliente
        if (l.current_client is None and (not priority_queue.empty() or not general_queue.empty())):
            if not priority_queue.empty():
                _, _, l.current_client = priority_queue.get()
            elif not general_queue.empty():
                l.current_client = general_queue.get()
            
            # Actualizar la lista y el turno actual
            self.clean_frame_turn()
            if l.current_client is not None:
                icon = ""
                if l.current_client.type == c.VIP:
                    icon = "👑"
                elif l.current_client.type == c.ONLINE:
                    icon = "🌐"
                else:
                    icon = "👥"

                ttk.Label(self.frame_turn, text="Turno Actual", style="SectionTitle.TLabel").pack(pady=(0, 5))
                ttk.Label(self.frame_turn, text=f"{icon}", font=("Arial", 16, "bold"), background="white", foreground="#333").pack()
                ttk.Label(self.frame_turn, text=f"#{l.current_client.id}", font=("Arial", 20), background="white", foreground="#333").pack(pady=5)
                ttk.Label(self.frame_turn, text=f"{l.current_client.name}", font=("Arial", 14), background="white", foreground="#333").pack()
            self.refresh_queue()
            add_action(c.CALL, l.current_client)
        
    def on_complete_service(self, event= None):
        if (l.current_client is not None):
            add_action(c.SERVICE_COMPLETED, l.current_client)
            l.current_client = None
            self.clean_frame_turn()
            ttk.Label(self.frame_turn, text="Turno Actual", style="SectionTitle.TLabel").pack(pady=(0, 5))
            ttk.Label(self.frame_turn, text="--", font=("Arial", 20, "bold"), background="white", foreground="#999").pack()
            ttk.Label(self.frame_turn, text="No hay turno activo", background="white", foreground="#999").pack(pady=5)



    def clean_frame_turn(self):
        for widget in self.frame_turn.winfo_children():
            widget.destroy()

    def on_undo(self, event=None):
        changed = undo()
        if changed:
            # Refrescar la lista y el turno actual
            self.refresh_queue()
            # Actualizar vista del turno actual según l.current_client
            self.clean_frame_turn()
            if l.current_client is not None:
                icon = ""
                if l.current_client.type == c.VIP:
                    icon = "👑"
                elif l.current_client.type == c.ONLINE:
                    icon = "🌐"
                else:
                    icon = "👥"

                ttk.Label(self.frame_turn, text="Turno Actual", style="SectionTitle.TLabel").pack(pady=(0, 5))
                ttk.Label(self.frame_turn, text=f"{icon}", font=("Arial", 16, "bold"), background="white", foreground="#333").pack()
                ttk.Label(self.frame_turn, text=f"#{l.current_client.id}", font=("Arial", 20), background="white", foreground="#333").pack(pady=5)
                ttk.Label(self.frame_turn, text=f"{l.current_client.name}", font=("Arial", 14), background="white", foreground="#333").pack()
            else:
                ttk.Label(self.frame_turn, text="Turno Actual", style="SectionTitle.TLabel").pack(pady=(0, 5))
                ttk.Label(self.frame_turn, text="--", font=("Arial", 20, "bold"), background="white", foreground="#999").pack()
                ttk.Label(self.frame_turn, text="No hay turno activo", background="white", foreground="#999").pack(pady=5)
    
    def on_menu(self, event=None):
        popup = ProductPopup(self.root, on_select=self.on_product_selected)
        popup.grab_set()

    def on_product_selected(self, product_id):
        self.products_added.append(product_id)


# IA
class TicketCard(ttk.Frame):
    def __init__(self, parent, number, name, ticket_id, type, order_size, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(style="Card.TFrame", padding=10)

        # === Número  de orden ===
        circle = tk.Frame(self, bg="#fff5ec", width=40, height=40)
        circle.pack(side="left", padx=(5, 15))
        circle.pack_propagate(False)
        tk.Label(circle, text=str(number), fg="#ff7b00", bg="#fff5ec", font=("Arial", 11, "bold")).pack(expand=True)

        # === Nombre y detalles ===
        info_frame = tk.Frame(self, bg="white")
        info_frame.pack(side="left", fill="x", expand=True)

        order_size_label = tk.Label(self, text=f"🛒 {order_size} productos", fg="#6a6a6a", bg="white", font=("Arial", 12))
        order_size_label.pack(side="right", fill="y")

        name_frame = tk.Frame(info_frame, bg="white")
        name_frame.pack(anchor="w")

        name_label = tk.Label(name_frame, text=name, font=("Arial", 11, "bold"), bg="white", fg="#222")
        name_label.pack(side="left")

        if type == c.VIP:
            vip_label = tk.Label(
                name_frame,
                text="👑 PRIORITARIO",
                bg="#fff1c1",
                fg="#a67c00",
                font=("Arial", 8, "bold"),
                padx=6, pady=2
            )
            vip_label.pack(side="left", padx=(8, 0))
        if type == c.ONLINE:
            vip_label = tk.Label(
                name_frame,
                text="🌐 DOMICILIO/ONLINE",
                bg="#fff1c1",
                fg="#a67c00",
                font=("Arial", 8, "bold"),
                padx=6, pady=2
            )
            vip_label.pack(side="left", padx=(8, 0))

        ticket_label = tk.Label(info_frame, text=f"Ticket #{ticket_id}", fg="#6a6a6a", bg="white", font=("Arial", 9))
        ticket_label.pack(anchor="w", pady=(3, 0))

        # Estilo del borde
        self.configure(style="TicketCard.TFrame")
# /IA
    
# IA
class ProductPopup(tk.Toplevel):
    def __init__(self, master=None, on_select=None):
        super().__init__(master)
        self.title("Selecciona un producto")
        self.geometry("400x300")
        self.configure(padx=20, pady=20)

        self.on_select = on_select

        # Cargar y redimensionar la imagen para ajustarla a los botones
        self.img1 = PhotoImage(file="./res/P001.png")
        self.img1 = self.img1.subsample(4, 4)

        self.img2 = PhotoImage(file="./res/P002.png")
        self.img2 = self.img2.subsample(4, 4)

        self.img3 = PhotoImage(file="./res/P003.png")
        self.img3 = self.img3.subsample(4, 4)

        # Cuadro 1 (arriba izquierda)
        self.product1 = tk.Button(self, image=self.img1, command=lambda: self.select_product("P001"))
        self.product1.grid(row=0, column=0, padx=10, pady=10)

        # Cuadro 2 (arriba derecha)
        self.product2 = tk.Button(self, image=self.img2, command=lambda: self.select_product("P002"))
        self.product2.grid(row=0, column=1, padx=10, pady=10)

        # Cuadro 3 (abajo izquierda)
        self.product3 = tk.Button(self, image=self.img3, command=lambda: self.select_product("P003"))
        self.product3.grid(row=1, column=0, padx=10, pady=10)

        # Botón "Completar"
        self.complete_button = tk.Button(self, text="✅ Completar", width=15, height=2, command=self.complete_selection)
        self.complete_button.grid(row=1, column=1, padx=10, pady=10)

    def select_product(self, product_id):
        if self.on_select:
            self.on_select(product_id)
        else:
            print(f"Seleccionaste el producto {product_id}")

    def complete_selection(self):
        self.destroy()
 # /IA
        

# Punto de entrada de la aplicación
if __name__ == "__main__":
    app = MainUI()
    app.root.mainloop()
    
