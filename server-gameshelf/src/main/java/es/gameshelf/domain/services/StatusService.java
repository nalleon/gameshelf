package es.gameshelf.domain.services;

import es.gameshelf.domain.Status;
import es.gameshelf.domain.interfaces.repository.IStatusRepository;
import es.gameshelf.domain.interfaces.service.IStatusService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * @author Nabil L. A. @nalleon
 */
@Service
public class StatusService implements IStatusService{
    /**
     * Properties
     */
    IStatusRepository repository;

    /**
     * Setter for the autowired service
     * @param repository of the service
     */
    @Autowired
    public void setRepository(IStatusRepository repository) {
        this.repository = repository;
    }

    @Override
    public Status add(String name, String description) {
        Status item = new Status();
        item.setName(name);
        item.setAdditionalText(description);

        return repository.save(item);
    }

    @Override
    public List<Status> findAll() {
        return repository.findAll();
    }

    @Override
    public Status findById(Integer id) {
        return repository.findById(id);
    }

    @Override
    public Status findByName(String name) {
        return repository.findByName(name);
    }

    @Override
    public boolean delete(Integer id) {
        return repository.delete(id);
    }

    @Override
    public Status update(Integer id, String name, String description) {
        Status item = new Status(id, name, description);

        return repository.update(item);
    }
}
